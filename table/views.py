from rest_framework import generics

from django.shortcuts import render
from .models import ResturantTable
from .serializers import ResturantTableSerializer

# Create your views here.
class ResturantTableListView(generics.ListCreateAPIView):
    queryset = ResturantTable.objects.all()
    serializer_class = ResturantTableSerializer