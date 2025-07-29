from django.contrib import admin
from .models import Room


class RoomAdmin(admin.ModelAdmin):
    # Columns shown in the list view
    list_display = (
        'number', 'room_type', 'get_display_price', 'status', 'is_available', 'floor', 'max_guests', 'created_at'
    )
    list_filter = ('room_type', 'status', 'is_available',
                   'floor', 'is_smoking_allowed', 'is_pet_friendly')
    search_fields = ('number', 'description')
    readonly_fields = ('created_at', 'updated_at')

    # Field groups for better organization in the form
    fieldsets = (
        ('Basic Information', {
            'fields': ('number', 'room_type', 'price_per_night', 'status', 'is_available')
        }),
        ('Room Details', {
            'fields': ('description', 'floor', 'size_sqm', 'max_guests')
        }),
        ('Amenities', {
            'fields': (
                'has_wifi', 'has_ac', 'has_tv', 'has_balcony', 'has_mountain_view',
                'has_stupa_view', 'has_private_bathroom', 'has_room_service',
                'has_kitchen', 'has_workspace'
            )
        }),
        ('Additional Features', {
            'fields': ('is_smoking_allowed', 'is_pet_friendly')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # Custom method to show price with currency in the list view
    def get_display_price(self, obj):
        return obj.get_display_price()
    get_display_price.short_description = "Price"


# Register the Room model with custom admin settings
admin.site.register(Room, RoomAdmin)
