from django.urls import path
from . import views


app_name = 'products'
urlpatterns = [
    path('add/category', views.add_category, name='add_category'),
    path('read', views.read_all_category, name='read'),
    path('products', views.ProductAPI.as_view(), name='product_read_write'),
    path('products/<int:pk>', views.ProductAPI.as_view(), name='product_edit'),
    path('update/<int:pk>', views.update_obj_category, name='update'),
    path('delete/<int:pk>', views.delete_category, name='delete')
]
