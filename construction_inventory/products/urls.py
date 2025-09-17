from django.urls import path, include
from . import views

app_name = 'products'

urlpatterns = [
    path('product-list/', views.ProductList.as_view(), name='product-list'),
    path('create-product/', views.CreateProduct.as_view(), name='create-product'),
    path('product-info/<int:pk>/', views.ProductDetail.as_view(), name='product-detail'),
    path('product-update/<int:pk>/', views.UpdateProduct.as_view(), name='update-product'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('manual-info/', views.Manual.as_view(), name='manual-info'),
]