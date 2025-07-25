from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'amount', 'method',
                  'timestamp', 'description', 'confirmed']
        read_only_fields = ['timestamp']
