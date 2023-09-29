from rest_framework import generics
from rest_framework import serializers


class FilesDataSerializer(serializers.Serializer):
   id = serializers.IntegerField()
   file_id = serializers.IntegerField()
   name = serializers.CharField(max_length=200)
   filename = serializers.CharField(max_length=100)
