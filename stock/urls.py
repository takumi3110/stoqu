from django.urls import path
from rest_framework import routers

from . import views

app_name = 'stock'

router = routers.DefaultRouter()
router.register(r'option', views.OptionViewSet)
router.register(r'storage', views.StorageItemViewSet)
router.register(r'kittingPlan', views.KittingPlanViewSet)
router.register(r'orderItem', views.OrderItemViewSet)
router.register(r'storageCart', views.StorageCartViewSet)
router.register(r'approve', views.ApproveViewSet)
router.register(r'orderInfo', views.OrderInfoViewSet)

urlpatterns = [
	path('', views.top_page, name='top'),
	path('item_list', views.StorageItemListView.as_view(), name='storage_list'),
	path('item_list_admin', views.StorageItemAdminListView.as_view(), name='storage_list_admin'),
	path('detail/<int:pk>', views.StorageItemDetailView.as_view(), name='storage_detail'),
	path('detail_admin/<int:pk>', views.StorageItemDetailAdminView.as_view(), name='storage_detail_admin'),
	path('get_data/', views.create_storage_data, name='get_data'),
	path('create/', views.StorageItemCreateView.as_view(), name='storage_create'),
	path('update/<int:pk>', views.StorageItemUpdateView.as_view(), name='storage_update'),
	path('optionCreate/', views.OptionCreateView.as_view(), name='option_create'),
	path('cart/', views.StorageCartView.as_view(), name='cart'),
	path('add_item/<int:pk>', views.add_item, name='add_item'),
	path('reduce_item/<int:pk>', views.reduce_cart, name='reduce_cart'),
	path('remove_item/<int:pk>', views.remove_cart, name='remove_cart'),
	path('approve/', views.ApproveView.as_view(), name='approve'),
	path('approve_create/', views.ApproveCreateView.as_view(), name='approve_create'),
	path('approve_update/<int:pk>', views.ApproveUpdateView.as_view(), name='approve_update'),
	path('add_orderInfo/', views.add_order_info, name='add_order_info'),
	path('confirm/<int:pk>', views.ConfirmView.as_view(), name='confirm'),
	path('my_order_info/', views.MyOrderInfoView.as_view(), name='my_order_info'),
	path('order_info_list/', views.OrderInfoListView.as_view(), name='orderinfo_list'),
	path('order_info_update/<int:pk>', views.OrderInfoUpdateView.as_view(), name='orderinfo_update'),
	path('order_info_detail/<int:pk>', views.OrderInfoDetailView.as_view(), name='orderinfo_detail'),
	path('order_info_detail_admin/<int:pk>', views.OrderInfoDetailAdminView.as_view(), name='orderinfo_detail_admin'),
	path('order_info_delete_select/<int:pk>', views.OrderInfoSelectView.as_view(), name='delete_select'),
	path('order_info_status/<int:pk>', views.order_info_status_view, name='orderinfo_status'),
	path('chang_quantity/<int:pk>', views.ChangeQuantity.as_view(), name='change_quantity'),
]
