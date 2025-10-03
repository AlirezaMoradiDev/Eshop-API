from django.urls import path
from . import views


app_name = 'products'
urlpatterns = [
    path('add', views.add_category, name='add'),
    path('read', views.read_all_category, name='read'),
    path('update/<int:pk>', views.update_obj_category, name='update'),
    path('delete/<int:pk>', views.delete_category, name='delete')
]