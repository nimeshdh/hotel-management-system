from django.contrib import admin
from .models import Review, ReviewImage, ReviewResponse


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'room', 'rating', 'category',
                    'is_approved', 'is_featured', 'created_at']
    list_filter = ['rating', 'category', 'is_approved',
                   'is_featured', 'is_verified_stay']
    search_fields = ['user__username', 'title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_approved', 'is_featured']

    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'room', 'title', 'content', 'rating', 'category')
        }),
        ('Stay Information', {
            'fields': ('stay_date', 'is_verified_stay')
        }),
        ('Status', {
            'fields': ('is_approved', 'is_featured', 'is_reported')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = ['review', 'caption', 'uploaded_at']
    search_fields = ['review__title', 'caption']


@admin.register(ReviewResponse)
class ReviewResponseAdmin(admin.ModelAdmin):
    list_display = ['review', 'responded_by', 'created_at']
    search_fields = ['review__title', 'content']
    readonly_fields = ['created_at']
