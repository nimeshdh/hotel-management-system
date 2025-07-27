from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, payment_list, payment_detail, invoice

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', include(router.urls)),
    path('list/', payment_list, name='payment_list'),
    path('detail/<int:payment_id>/', payment_detail, name='payment_detail'),
    path('invoice/<int:payment_id>/', invoice, name='invoice'),
]
