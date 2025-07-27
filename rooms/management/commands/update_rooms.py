from django.core.management.base import BaseCommand
from rooms.models import Room
from services.models import Service
from django.db import connection


class Command(BaseCommand):
    help = 'Update existing rooms with new fields and create sample data'

    def handle(self, *args, **options):
        self.stdout.write('Starting Via-Via Boutique Hotel data update...')

        # First, let's add the missing columns manually
        with connection.cursor() as cursor:
            try:
                # Add missing columns to rooms table
                cursor.execute("""
                    ALTER TABLE rooms_room 
                    ADD COLUMN status VARCHAR(20) DEFAULT 'available'
                """)
                self.stdout.write('Added status column')
            except Exception as e:
                self.stdout.write(f'Status column might already exist: {e}')

            try:
                cursor.execute("""
                    ALTER TABLE rooms_room 
                    ADD COLUMN floor INTEGER DEFAULT 1
                """)
                self.stdout.write('Added floor column')
            except Exception as e:
                self.stdout.write(f'Floor column might already exist: {e}')

            try:
                cursor.execute("""
                    ALTER TABLE rooms_room 
                    ADD COLUMN size_sqm INTEGER DEFAULT 30
                """)
                self.stdout.write('Added size_sqm column')
            except Exception as e:
                self.stdout.write(f'Size_sqm column might already exist: {e}')

            try:
                cursor.execute("""
                    ALTER TABLE rooms_room 
                    ADD COLUMN max_guests INTEGER DEFAULT 2
                """)
                self.stdout.write('Added max_guests column')
            except Exception as e:
                self.stdout.write(
                    f'Max_guests column might already exist: {e}')

            # Add boolean columns
            boolean_columns = [
                'has_wifi', 'has_ac', 'has_tv', 'has_balcony', 'has_mountain_view',
                'has_stupa_view', 'has_private_bathroom', 'has_room_service',
                'is_smoking_allowed', 'is_pet_friendly', 'has_kitchen', 'has_workspace'
            ]

            for col in boolean_columns:
                try:
                    cursor.execute(f"""
                        ALTER TABLE rooms_room 
                        ADD COLUMN {col} BOOLEAN DEFAULT FALSE
                    """)
                    self.stdout.write(f'Added {col} column')
                except Exception as e:
                    self.stdout.write(f'{col} column might already exist: {e}')

            # Set default values for existing rooms
            cursor.execute("""
                UPDATE rooms_room 
                SET has_wifi = TRUE, has_ac = TRUE, has_tv = TRUE, 
                    has_private_bathroom = TRUE, has_room_service = TRUE
                WHERE has_wifi IS NULL
            """)

            # Update room types to match new choices
            cursor.execute("""
                UPDATE rooms_room 
                SET room_type = 'single' WHERE room_type = 'Single'
            """)
            cursor.execute("""
                UPDATE rooms_room 
                SET room_type = 'double' WHERE room_type = 'Double'
            """)
            cursor.execute("""
                UPDATE rooms_room 
                SET room_type = 'suite' WHERE room_type = 'Suite'
            """)
            cursor.execute("""
                UPDATE rooms_room 
                SET room_type = 'deluxe' WHERE room_type = 'Deluxe'
            """)

        # Now update existing rooms with proper data
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
            self.stdout.write(f'Updated room {room.number}')

        # Create additional enhanced rooms
        enhanced_rooms_data = [
            {
                'number': '301',
                'room_type': 'suite',
                'price_per_night': 180.00,
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
                'price_per_night': 120.00,
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
                'price_per_night': 150.00,
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
                'price_per_night': 45.00,
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
                self.stdout.write(
                    f'Created room: {room.number} - {room.get_room_type_display()}')
            else:
                self.stdout.write(f'Room already exists: {room.number}')

        # Create sample services
        services_data = [
            {
                'name': 'Traditional Nepali Breakfast',
                'description': 'Start your day with authentic Nepali breakfast including dal bhat, roti, and masala tea.',
                'category': 'food',
                'price': 15.00,
                'duration_minutes': 60,
                'location': 'Rooftop Restaurant',
                'is_available_24_7': False,
            },
            {
                'name': 'Tibetan Massage Therapy',
                'description': 'Relaxing traditional Tibetan massage using natural oils and techniques.',
                'category': 'wellness',
                'price': 45.00,
                'duration_minutes': 90,
                'location': 'Spa Center',
                'is_available_24_7': False,
            },
            {
                'name': 'Airport Transfer',
                'description': 'Comfortable transfer from Tribhuvan International Airport to the hotel.',
                'category': 'transport',
                'price': 25.00,
                'duration_minutes': 45,
                'location': 'Airport to Hotel',
                'is_available_24_7': True,
            },
            {
                'name': 'Boudhanath Stupa Tour',
                'description': 'Guided tour of the sacred Boudhanath Stupa with cultural insights.',
                'category': 'tours',
                'price': 20.00,
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
                self.stdout.write(f'Created service: {service.name}')
            else:
                self.stdout.write(f'Service already exists: {service.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ All data updated successfully!\n'
                f'Total rooms: {Room.objects.count()}\n'
                f'Total services: {Service.objects.count()}'
            )
        )
