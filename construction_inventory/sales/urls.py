from django.urls import path, include
from . import views

app_name = 'sales'

urlpatterns = [
    path('', views.SaleList.as_view(), name='sales-list'),
    path('create-sale/', views.SaleCreate.as_view(), name='create-sale'),
]