from rest_framework import generics
from django.shortcuts import render

from .models import Reservation
from .serializers import ReservationSerializer

# Create your views here.
class ReservationListView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer