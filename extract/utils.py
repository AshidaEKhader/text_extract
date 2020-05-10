import collections
import os
import re
from operator import *

from django.conf import settings
from nltk import regexp_tokenize
from nltk.corpus import stopwords
from rest_framework import exceptions

# Instantiate a dictionary, and for every word in the file,
# Add to the dictionary if it doesn't exist. If it does, increase the count.
wordcount = {}


def get_file_data(files):
    """
    Function that finds the popular words in the input file
    :param files:
    :return: a dict of words containing number of occurrence of it , lines of the occurrence and files in which it appeared.
    E.g: {'Django':{'count': 2, 'files': ['file1','file2'], lines: ['Hi Django', 'Hello Django']}}
    """
    try:
        #: Pattern for words
        pattern = r'''[A-Z]{2,}(?![a-z])|[A-Z][a-z]\.+(?=[A-Z])|[\'\w\-]+'''

        # Read input files one by one, note the encoding is specified here
        # It may be different in your text file
        for file in files:
            file_name = file.name
            #: Read the contents of file
            content = file.file.readlines()
            # you may also want to remove whitespace characters like `\n` at the end of each line
            content = [x.strip() for x in content]
            for line in content:
                #: The line is tokenized based on the pattern specified
                word_tokens = regexp_tokenize(line.decode('utf-8'), pattern)
                get_popular_words(word_tokens, file_name, line)

        # Find most frequent interesting words,
        # i.e, words having occurrence more than WORD_COUNT_THRESHOLD
        common_interesting_words = {k: v for k, v in wordcount.items() if v['count'] > settings.WORD_COUNT_THRESHOLD}

        #: Sort the common_interesting_words with the most common word taking first position,
        # i.e, in descending order of count
        sorted_word_dict = collections.OrderedDict(sorted(common_interesting_words.items(), key=lambda x: getitem(x[1],
                                                                                                                  'count'),
                                                          reverse=True))
        return sorted_word_dict
    except Exception as e:
        raise exceptions.ValidationError(e, 400)


def get_stop_words():
    """
    Function to find stop words and common words in English. Also appending punctuations to the set
    :return: stop_word_set - A set containing stop words, common words and punctuations
    """
    # Stopwords
    stop_word_set = set(stopwords.words('english'))
    # os.path.join(settings.BASE_DIR, 'extract')
    file_ = open(os.path.join(settings.BASE_DIR, 'extract/common_words.txt'))
    #: Open common_words.txt file which contains common words in English
    with open(os.path.join(settings.BASE_DIR, 'extract/common_words.txt')) as f:
        wordset = set()
        for line in f:
            #: To read the content of file line by line, spilt the file content with line delimiters like .;?!\n
            wordset.add(line.strip())

    #: Combine the sets
    stop_word_set.update(wordset)
    return stop_word_set


def get_popular_words(word_tokens, file_name, line):
    #: function call to get the common words and symbols
    stop_word_set = get_stop_words()
    for word in word_tokens:
        #: To avoid duplication due to case(upper case and lower case)
        word = word.lower()
        # : Check if the word is not a stop word, then call adding_popular_words()
        if word not in stop_word_set:
            adding_popular_words(word, file_name, line)


def adding_popular_words(word, file_name, line):
    """
    Function to save popular words to the dict
    :param: word
    :param: file_name
    :param: line
    :return:
    """
    #: Check if the word is an actual english word(not number or patterns like --, ** etc..)
    # else omit it.
    if re.match(r'[a-zA-Z]+', word):
        #: To capitalize first letter of word
        word = word.capitalize()
        #: If word is an actual english word and not exist in wordcount , the word is added to dict along with file name
        # and the line else we are incrementing the 'count' of the word, appending the new line in which occur and
        # file_name if it's on other file
        if word not in wordcount:
            wordcount[word] = dict(count=1, file_name=[file_name], lines=[line])
        else:
            wordcount[word]['count'] += 1
            if file_name not in wordcount[word]['file_name']:
                wordcount[word]['file_name'].append(file_name)
            wordcount[word]['lines'].append(line)