from django.shortcuts import render
from rest_framework import generics

from .models import Payment
from .serializers import PaymentSerializer

# Create your views here.

class PaymentListView(generics.ListCreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer