from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .serializers import BookingSerializer
from rooms.models import Room


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


@login_required
def booking_form(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        guests = request.POST.get('guests', 1)

        if check_in and check_out:
            booking = Booking.objects.create(
                user=request.user,
                room=room,
                check_in=check_in,
                check_out=check_out,
                guests=guests,
                status='pending'
            )
            messages.success(request, 'Booking created successfully!')
            return redirect('booking_detail', booking_id=booking.id)
        else:
            messages.error(request, 'Please fill all required fields.')

    return render(request, 'bookings/booking_form.html', {'room': room})


@login_required
def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(
        user=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})
