from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('text_gen/', include('text_gen.urls')),
    path('admin/', admin.site.urls),
]