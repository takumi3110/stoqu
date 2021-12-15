from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from .settings.base import MEDIA_URL, MEDIA_ROOT
from device.urls import router as device_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/device/', include(device_router.urls)),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(MEDIA_URL, documment_root=MEDIA_ROOT)
