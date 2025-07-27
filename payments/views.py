from rest_framework import viewsets
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Payment
from .serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


@login_required
def payment_list(request):
    payments = Payment.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'payments/payment_list.html', {'payments': payments})


@login_required
def payment_detail(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    return render(request, 'payments/payment_detail.html', {'payment': payment})


@login_required
def invoice(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id, user=request.user)
    
    # This is a simplified example. In a real application, you would
    # fetch more details related to this payment, such as booking information.
    context = {
        'invoice_number': f"INV-{payment.id:06d}",
        'customer_name': payment.user.get_full_name() or payment.user.username,
        'amount': payment.amount,
        'status': 'success' if payment.confirmed else 'pending',
    }
    
    return render(request, 'payments/invoice.html', context)
