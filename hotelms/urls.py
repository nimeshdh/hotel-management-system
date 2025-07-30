"""
URL configuration for hotelms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rooms import views as room_views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views


# Add these new URL patterns to your existing urlpatterns list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('about/', room_views.about, name='about'), # Changed views.about to room_views.about
    path('api/users/', include('users.urls')),
    path('api/services/', include('services.urls')),
    path('api/rooms/', include('rooms.urls')),
    path('api/payments/', include('payments.urls')),
    path('api/bookings/', include('bookings.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('', room_views.home, name='home'),
    path('about/', room_views.about, name='about'),
    path('rooms/', room_views.rooms, name='rooms'),
    path('rooms/<int:pk>/', room_views.room_detail, name='room_detail'),
    path('bookings/', include('bookings.urls')),
    path('services/', include('services.urls')),
    path('reviews/', include('reviews.urls')),
    path('login/', user_views.user_login, name='login'),
    path('register/', user_views.user_register, name='register'),
    path('logout/', user_views.user_logout, name='logout'),
    path('payments/', include('payments.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
