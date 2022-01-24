from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('room/<str:pk>/', views.room, name='room'),
    path('edit-room/<str:pk>/', views.editRoom, name='edit-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    path('create-room', views.createRoom, name='create-room'),
]
