from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    # Columns shown in the list view
    list_display = ('id', 'user', 'amount', 'method', 'confirmed', 'timestamp')
    list_filter = ('method', 'confirmed', 'timestamp')
    search_fields = ('user__username', 'description')
    readonly_fields = ('timestamp',)

    fieldsets = (
        ('Payment Information', {
            'fields': ('user', 'amount', 'method', 'description')
        }),
        ('Status', {
            'fields': ('confirmed',)
        }),
        ('Timestamps', {
            'fields': ('timestamp',)
        }),
    )

    # Customize ordering
    ordering = ('-timestamp',)


# Register Payment model with admin site
admin.site.register(Payment, PaymentAdmin)
