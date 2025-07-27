from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookingViewSet, booking_form, booking_detail, my_bookings

router = DefaultRouter()
router.register(r'bookings', BookingViewSet, basename='booking')

urlpatterns = [
    # Web routes
    path('create/<int:room_id>/', booking_form, name='booking_form'),
    path('<int:booking_id>/', booking_detail, name='booking_detail'),
    path('', my_bookings, name='my_bookings'),

    # API routes
    path('api/', include(router.urls)),
]
