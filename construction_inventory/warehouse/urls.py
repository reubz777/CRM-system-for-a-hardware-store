from django.urls import path
from . import views

app_name = 'warehouse'

urlpatterns = [
    path('', views.BatchList.as_view(), name='batch-list'),
    path('create-batch/', views.CreateBatch.as_view(), name='create-batch'),
    path('delete-batch/<int:pk>/', views.DeleteBatch.as_view(), name='delete-batch'),
    path('edit-batch/<int:pk>/', views.BatchUpdateInfo.as_view(), name='edit-batch'),
    path('consolidation-batch/<int:pk>/', views.ConsolidationBatch.as_view(), name='consolidation-batch'),
    path('export-xml/', views.export_xlsx, name='export-xml'),
]