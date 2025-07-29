from django.contrib import admin
from users.models import CustomUser
from rooms.models import Room
from services.models import Service
from payments.models import Payment
from django.contrib.auth.admin import UserAdmin


# Custom Admin for Users
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'role',
                    'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name',
         'last_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'phone', 'address'),
        }),
    )
    ordering = ('username',)


# Custom Admin for Rooms
class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'room_type', 'get_display_price',
                    'status', 'is_available', 'floor', 'max_guests', 'created_at')
    list_filter = ('room_type', 'status', 'is_available',
                   'floor', 'is_smoking_allowed', 'is_pet_friendly')
    search_fields = ('number', 'description')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {'fields': ('number', 'room_type',
         'price_per_night', 'status', 'is_available')}),
        ('Details', {'fields': ('description',
         'floor', 'size_sqm', 'max_guests')}),
        ('Amenities', {
            'fields': ('has_wifi', 'has_ac', 'has_tv', 'has_balcony', 'has_mountain_view', 'has_stupa_view',
                       'has_private_bathroom', 'has_room_service', 'has_kitchen', 'has_workspace')
        }),
        ('Extra', {'fields': ('is_smoking_allowed', 'is_pet_friendly')}),
        ('Image', {'fields': ('image',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def get_display_price(self, obj):
        return obj.get_display_price()
    get_display_price.short_description = "Price"


# Custom Admin for Services
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'get_display_price', 'is_active',
                    'is_available_24_7', 'requires_advance_booking', 'created_at')
    list_filter = ('category', 'is_active', 'is_available_24_7',
                   'requires_advance_booking')
    search_fields = ('name', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Info', {
         'fields': ('name', 'description', 'category', 'price', 'image')}),
        ('Availability', {'fields': ('is_active', 'is_available_24_7',
         'requires_advance_booking', 'advance_booking_hours')}),
        ('Details', {'fields': ('duration_minutes', 'max_capacity', 'location')}),
        ('Additional Info', {'fields': ('terms_conditions',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )

    def get_display_price(self, obj):
        return obj.get_display_price()
    get_display_price.short_description = "Price"


# Custom Admin for Payments
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'method', 'confirmed', 'timestamp')
    list_filter = ('method', 'confirmed', 'timestamp')
    search_fields = ('user__username', 'description')
    readonly_fields = ('timestamp',)

    fieldsets = (
        ('Payment Info', {
         'fields': ('user', 'amount', 'method', 'description')}),
        ('Status', {'fields': ('confirmed',)}),
        ('Timestamps', {'fields': ('timestamp',)}),
    )


# Register all models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Payment, PaymentAdmin)
