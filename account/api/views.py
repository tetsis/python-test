from django.shortcuts import render
from rest_framework import viewsets
from .models import Table
from .serializer import TableSerializer, TablesSerializer

# Create your views here.

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class TablesViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TablesSerializer
