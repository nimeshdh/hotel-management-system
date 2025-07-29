from django.contrib import admin
from .models import Service


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'get_display_price', 'is_active', 'is_available_24_7', 'requires_advance_booking', 'created_at'
    )
    list_filter = ('category', 'is_active', 'is_available_24_7',
                   'requires_advance_booking')
    search_fields = ('name', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'price', 'image')
        }),
        ('Service Availability', {
            'fields': ('is_active', 'is_available_24_7', 'requires_advance_booking', 'advance_booking_hours')
        }),
        ('Service Details', {
            'fields': ('duration_minutes', 'max_capacity', 'location')
        }),
        ('Additional Information', {
            'fields': ('terms_conditions',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    # Make get_display_price available in admin list
    def get_display_price(self, obj):
        return obj.get_display_price()
    get_display_price.short_description = "Price"


# Register the Service model
admin.site.register(Service, ServiceAdmin)
