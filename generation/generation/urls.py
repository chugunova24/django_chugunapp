from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import socket  # only if you haven't already imported this
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('file-reader/', include('text_gen.urls')),
]


if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
    # urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + ["127.0.0.1", "10.0.2.2"]