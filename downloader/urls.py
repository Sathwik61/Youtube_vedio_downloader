from django.urls import path
from .views import youtube, download_file

urlpatterns = [
    path('', youtube, name='youtube'),
    path('download/<str:file_name>/', download_file, name='download_file'),
]
