from django.urls import path, include
from . import views

app_name = 'categories'

urlpatterns = [
    path('', views.CategoryList.as_view(), name='category-list'),
    path('create-category/', views.CreateCategory.as_view(), name='create-category'),
    path('delete-category/<int:pk>', views.DeleteCategory.as_view(), name='delete-category'),
    path('edit-category/<int:pk>', views.EditCategory.as_view(), name='edit-category'),

]