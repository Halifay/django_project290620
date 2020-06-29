from django.urls import path
from . import views

app_name = 'receiver'
urlpatterns = [
    path('', views.index, name='index'),
    path('transaction/<int:transaction_id>/', views.tn_detail, name='detail'),
    path('customer/<int:customer_id>/', views.cr_info, name='info'),
    path('get_five/', views.get_five, name='get_five'),
    path('upload-csv/', views.transaction_upload, name='csv_upload')
]