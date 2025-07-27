#!/usr/bin/env python
from django.utils import timezone
from services.models import Service
from rooms.models import Room
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotelms.settings')
django.setup()


def update_existing_rooms():
    """Update existing rooms with new fields"""
    print("Updating existing rooms...")

    # Get all existing rooms
    rooms = Room.objects.all()

    for room in rooms:
        # Set default values for new fields
        if not hasattr(room, 'status') or room.status is None:
            room.status = 'available'

        if not hasattr(room, 'floor') or room.floor is None:
            room.floor = 1

        if not hasattr(room, 'max_guests') or room.max_guests is None:
            if room.room_type == 'single':
                room.max_guests = 1
            elif room.room_type == 'double':
                room.max_guests = 2
            elif room.room_type == 'suite':
                room.max_guests = 4
            else:
                room.max_guests = 2

        if not hasattr(room, 'size_sqm') or room.size_sqm is None:
            if room.room_type == 'single':
                room.size_sqm = 25
            elif room.room_type == 'double':
                room.size_sqm = 35
            elif room.room_type == 'suite':
                room.size_sqm = 60
            else:
                room.size_sqm = 30

        # Set amenities based on room type
        if room.room_type == 'suite':
            room.has_balcony = True
            room.has_mountain_view = True
            room.has_kitchen = True
            room.has_workspace = True
        elif room.room_type == 'deluxe':
            room.has_balcony = True
            room.has_mountain_view = True

        # Set stupa view for some rooms
        if room.number in ['101', '102', '201', '202']:
            room.has_stupa_view = True

        room.save()
        print(f"Updated room {room.number}")


def create_sample_services():
    """Create sample hotel services"""
    print("Creating sample services...")

    services_data = [
        {
            'name': 'Traditional Nepali Breakfast',
            'description': 'Start your day with authentic Nepali breakfast including dal bhat, roti, and masala tea.',
            'category': 'food',
            'price': 2500,
            'duration_minutes': 60,
            'location': 'Rooftop Restaurant',
            'is_available_24_7': False,
        },
        {
            'name': 'Tibetan Massage Therapy',
            'description': 'Relaxing traditional Tibetan massage using natural oils and techniques.',
            'category': 'wellness',
            'price': 4500,
            'duration_minutes': 90,
            'location': 'Spa Center',
            'is_available_24_7': False,
        },
        {
            'name': 'Airport Transfer',
            'description': 'Comfortable transfer from Tribhuvan International Airport to the hotel.',
            'category': 'transport',
            'price': 6000,
            'duration_minutes': 45,
            'location': 'Airport to Hotel',
            'is_available_24_7': True,
        },
        {
            'name': 'Boudhanath Stupa Tour',
            'description': 'Guided tour of the sacred Boudhanath Stupa with cultural insights.',
            'category': 'tours',
            'price': 4000,
            'duration_minutes': 120,
            'location': 'Boudhanath Stupa',
            'is_available_24_7': False,
        },
        {
            'name': 'Daily Housekeeping',
            'description': 'Professional daily cleaning and room maintenance service.',
            'category': 'housekeeping',
            'price': 0.00,  # Free service
            'duration_minutes': 30,
            'location': 'Guest Rooms',
            'is_available_24_7': False,
        },
        {
            'name': 'Concierge Services',
            'description': 'Personal assistance with bookings, recommendations, and local information.',
            'category': 'concierge',
            'price': 0.00,  # Free service
            'duration_minutes': None,
            'location': 'Front Desk',
            'is_available_24_7': True,
        },
    ]

    for service_data in services_data:
        service, created = Service.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        if created:
            print(f"Created service: {service.name}")
        else:
            print(f"Service already exists: {service.name}")


def create_enhanced_rooms():
    """Create additional enhanced rooms for the boutique hotel"""
    print("Creating enhanced rooms...")

    enhanced_rooms_data = [
        {
            'number': '301',
            'room_type': 'suite',
            'price_per_night': 10000,
            'description': 'Luxurious executive suite with panoramic views of the Himalayas and Boudhanath Stupa. Features a separate living area, kitchenette, and private balcony.',
            'floor': 3,
            'size_sqm': 75,
            'max_guests': 4,
            'has_balcony': True,
            'has_mountain_view': True,
            'has_stupa_view': True,
            'has_kitchen': True,
            'has_workspace': True,
        },
        {
            'number': '302',
            'room_type': 'deluxe',
            'price_per_night': 12000,
            'description': 'Spacious deluxe room with modern amenities and stunning mountain views. Perfect for couples seeking comfort and luxury.',
            'floor': 3,
            'size_sqm': 45,
            'max_guests': 2,
            'has_balcony': True,
            'has_mountain_view': True,
            'has_stupa_view': False,
        },
        {
            'number': '401',
            'room_type': 'family',
            'price_per_night': 15000,
            'description': 'Family room with connecting areas, perfect for families with children. Features multiple beds and a spacious bathroom.',
            'floor': 4,
            'size_sqm': 55,
            'max_guests': 4,
            'has_balcony': False,
            'has_mountain_view': True,
        },
        {
            'number': '501',
            'room_type': 'budget',
            'price_per_night': 5000,
            'description': 'Comfortable budget room with essential amenities. Great value for solo travelers or budget-conscious guests.',
            'floor': 5,
            'size_sqm': 20,
            'max_guests': 1,
            'has_balcony': False,
            'has_mountain_view': False,
        },
    ]

    for room_data in enhanced_rooms_data:
        room, created = Room.objects.get_or_create(
            number=room_data['number'],
            defaults=room_data
        )
        if created:
            print(
                f"Created room: {room.number} - {room.get_room_type_display()}")
        else:
            print(f"Room already exists: {room.number}")


if __name__ == '__main__':
    print("Starting Via-Via Boutique Hotel data update...")

    try:
        update_existing_rooms()
        create_sample_services()
        create_enhanced_rooms()

        print("\n✅ All data updated successfully!")
        print(f"Total rooms: {Room.objects.count()}")
        print(f"Total services: {Service.objects.count()}")

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
