from django.urls import path
from . import views

app_name = 'supplies'

urlpatterns = [
    path('', views.SuppliesList.as_view(),name='supplies-list'),
    path('create-supplies/', views.SuppliesAdd.as_view(), name='create-supplies'),
    path('edit-supplies/<int:pk>/', views.SuppliesEdit.as_view(), name='edit-supplies'),
    path('delete-supplies/<int:pk>/', views.SuppliesDelete.as_view(), name='delete-supplies'),

]