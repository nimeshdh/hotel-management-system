from django.contrib import admin
from .models import Booking


class BookingAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('id', 'user', 'room', 'check_in',
                    'check_out', 'guests', 'status', 'created_at')
    list_filter = ('status', 'check_in', 'check_out', 'created_at')
    search_fields = ('user__username', 'room__number')
    readonly_fields = ('created_at',)

    # Organizing fields in sections
    fieldsets = (
        ('Booking Info', {
            'fields': ('user', 'room', 'services', 'status')
        }),
        ('Dates', {
            'fields': ('check_in', 'check_out')
        }),
        ('Guest Info', {
            'fields': ('guests',)
        }),
        ('Timestamps', {
            'fields': ('created_at',)
        }),
    )

    # Enable filter horizontal for ManyToManyField (services)
    filter_horizontal = ('services',)

    ordering = ('-created_at',)


# Register the Booking model
admin.site.register(Booking, BookingAdmin)
