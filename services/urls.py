from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ServicePageView

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', ServicePageView.as_view(), name='service_list'),
]
