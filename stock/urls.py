from django.urls import path
from rest_framework import routers

from . import views

app_name = 'stock'

router = routers.DefaultRouter()
router.register(r'option', views.OptionViewSet)
router.register(r'base', views.BaseViewSet)
router.register(r'storage', views.StorageItemViewSet)
router.register(r'kittingPlan', views.KittingPlanViewSet)
router.register(r'orderItem', views.OrderItemViewSet)
router.register(r'storageCart', views.StorageCartViewSet)
router.register(r'approve', views.ApproveViewSet)
router.register(r'orderInfo', views.OrderInfoViewSet)

urlpatterns = [
	path('', views.StorageItemListView.as_view(), name='storage_list'),
	path('detail/<int:pk>', views.StorageItemDetailView.as_view(), name='storage_detail'),
	path('get_data/', views.create_storage_data, name='get_data'),
	path('create/', views.StorageItemCreateView.as_view(), name='storage_create'),
	path('update/<int:pk>', views.StorageItemUpdateView.as_view(), name='storage_update'),
	path('optionCreate/', views.OptionCreateView.as_view(), name='option_create'),
	path('cart_list/', views.StorageCartListView.as_view(), name='cart'),
	path('add_item/<int:pk>', views.add_item, name='add_item'),
	path('reduce_item/<int:pk>', views.reduce_cart, name='reduce_cart'),
	path('remove_item/<int:pk>', views.remove_cart, name='remove_cart'),
	path('approve/', views.ApproveView.as_view(), name='approve'),
	path('approve_create/', views.ApproveCreateView.as_view(), name='approve_create'),
	path('approve_update/<int:pk>', views.ApproveUpdateView.as_view(), name='approve_update'),
	path('add_orderInfo/', views.add_order_info, name='add_order_info'),
	path('confirm/<int:pk>', views.ConfirmView.as_view(), name='confirm'),
	path('my_order_info/', views.MyOrderInfoView.as_view(), name='my_order_info'),
	path('order_info_detail/<int:pk>', views.OrderInfoDetailView.as_view(), name='order_info_detail'),
]
