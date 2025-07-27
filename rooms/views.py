from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from rest_framework import viewsets
from .models import Room
from .serializers import RoomSerializer


class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


def home(request):
    return render(request, 'home.html')


def rooms(request):
    room_list = [
        {"name": "Deluxe Room", "price": 100,
            "description": "Spacious room with sea view"},
        {"name": "Suite", "price": 200, "description": "Luxury suite with living room"},
        {"name": "Standard Room", "price": 50,
            "description": "Basic room with essential amenities"},
    ]
    return render(request, 'rooms.html', {'rooms': room_list})


def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms/room_list.html', {'rooms': rooms})


def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'rooms/room_details.html', {'room': room})
