from rest_framework import serializers
from .models import Booking
from rooms.models import Room
from rooms.serializers import RoomSerializer  
from services.models import Service
from services.serializers import ServiceSerializer  
from django.contrib.auth import get_user_model

User = get_user_model()


class BookingSerializer(serializers.ModelSerializer):
    services = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True,
        required=False
    )
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())


    services_detail = ServiceSerializer(
        source='services', many=True, read_only=True)
    room_detail = RoomSerializer(source='room', read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'user', 'room', 'services', 'services_detail',
            'room_detail', 'check_in', 'check_out', 'guests', 'status', 'created_at'
        ]
        read_only_fields = ['created_at', 'services_detail', 'room_detail']
