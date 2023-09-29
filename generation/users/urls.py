from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('register/', user_views.RegisterUserView.as_view(), name='register'),
    path('profile/', user_views.ProfileView.as_view(), name='profile'),

    path('login/', user_views.LoginUserView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', user_views.logout_user, name='logout'),
]


# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# 	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
