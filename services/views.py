from rest_framework import viewsets
from .models import Service
from .serializers import ServiceSerializer
from django.views.generic import TemplateView


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServicePageView(TemplateView):
    template_name = 'services/services.html'
