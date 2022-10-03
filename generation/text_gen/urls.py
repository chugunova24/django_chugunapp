from django.urls import path

from . import views
from .views import TextGenAPIView, TranslatorAPIView

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex /text_gen/api/v1/metrics
    path('api/v1/textgen', TextGenAPIView.as_view()),
    path('api/v1/transl', TranslatorAPIView.as_view())
]