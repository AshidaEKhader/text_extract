import logging

from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response

from .utils import get_file_data

logger = logging.getLogger(__name__)
# Create your views here.

class ExtractView(RetrieveAPIView):
    """
     API view for listing popular texts in the files inputted
    """
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        """
        Method to retrieve all the popular words from the files.
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        #: Read all the files inputted by user
        files = request.data.getlist('docs')
        #: Function call to get popular words in the docs passed
        data = get_file_data(files)
        response = Response(data, status=status.HTTP_200_OK)
        return response
