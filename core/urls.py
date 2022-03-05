from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.index, name='index'),
    path('room/<str:pk>/', views.room, name='room'),

    path('create-room', views.createRoom, name='create-room'),
    path('edit-room/<str:pk>/', views.editRoom, name='edit-room'),
    path('deleteroom/<str:pk>/', views.deleteRoom, name='delete-room'),
    
    path('deletemessage/<str:pk>/', views.deleteMessage, name='delete-message'),
]
