from django.contrib import admin
from django.urls import path, include

from device.urls import router as device_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/device/', include(device_router.urls)),
]
