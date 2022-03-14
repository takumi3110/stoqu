from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns

from .settings.base import MEDIA_URL, MEDIA_ROOT
from device.urls import router as device_router
from stock.urls import router as stock_router
from user.urls import router as user_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/device/', include(device_router.urls)),
    path('api/v1/stock/', include(stock_router.urls)),
    path('api/v1/user/', include(user_router.urls)),
    path('', include('stock.urls')),
    path('quote/', include('quote.urls')),
    path('device/', include('device.urls')),
    path('user/', include('user.urls'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
