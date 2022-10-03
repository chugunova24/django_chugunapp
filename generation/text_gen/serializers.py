from rest_framework import generics
from rest_framework import serializers

from .models import TextGen, Translator

class TextGenSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextGen
        fields = '__all__'   #['generation_text']

    # def create(self, validated_data):


class TranslatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translator
        fields = '__all__'   #['generation_text']


