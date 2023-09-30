from django.urls import path
from django.urls import re_path

from . import views
# from .views import TextGenAPIView, TranslatorAPIView\

# app_name = "users"

urlpatterns = [
    path('home', views.home, name="home"),
    path('about-me', views.about_me, name="about-me"),
    path('csv-reader-home/', views.CsvReaderHome.as_view(), name="csv-reader-home"),
    # path('csv-reader-filter', views.csv_reader_filter, name="csv-reader-filter"),
    path('csv-reader-filter', views.CsvReaderFilter.as_view(), name="csv-reader-filter"),
    # re_path(r'csv-reader-filter?selected_file=<int:id_file>/$', views.CsvReaderFilter.as_view(), name="csv-reader-filter"),


    # path('upload-files', views.upload_file, name="upload-files"),
    # path('filter-files', views.filter_user_files, name="filter-files"),
]