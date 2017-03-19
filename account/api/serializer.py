from rest_framework import serializers
from .models import Table

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'name', 'password')

class TablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ('id', 'name')
        read_only=True
