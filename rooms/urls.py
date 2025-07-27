from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet
from . import views
router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')

urlpatterns = [
    path('', include(router.urls)),
    path('', views.home, name='home'),  # Optional homepage
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:pk>/', views.room_detail, name='room_detail'),
]
