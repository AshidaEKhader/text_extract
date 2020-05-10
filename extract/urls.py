
from django.urls import path;
from .views import ExtractView;

#: Extract URL

urlpatterns = [
    path('popular_text/list', ExtractView.as_view(), name='get_popular_text_list')
]