from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response

# from predict import generate_blabla
from .GPT.generation import GPT
from .models import Metrics, TextGen, Translator
from .MarianMTModel.translator import TranslatedText
from .serializers import TextGenSerializer, TranslatorSerializer

import torch
# from text_gen.lstm_nn.preprocessing_data import evaluate, word_to_idx, idx_to_word
# from text_gen.models import TextGen


# model_load = torch.load('./text_gen/lstm_nn/weight/model_all')

def index(request):
    return HttpResponse('Hello, dudes')


class TextGenAPIView(generics.ListAPIView):
    # queryset = TextGen.objects.all()
    serializer_class = TextGenSerializer

    def get_queryset(self):
        queryset = TextGen.objects.all()
        return queryset


    def get(self, request, *args, **kwargs):
        return Response({'error': 'GET-запрос не поддерживается'})

    def post(self, request):
        input = request.data['input']
        min_length = len(input.split())
        max_length = request.data['max_length']

        try:
            translated_text_ru = TranslatedText(input).translate_ru()
            obj = GPT(translated_text_ru, min_length, max_length)
            generation_text = obj.get_sentence()

            translated_text = TranslatedText(generation_text).translate_en()

            if (min_length and max_length) > 0 and (max_length < 600):
                TextGen.objects.create(
                    input=input,
                    min_length=min_length,
                    max_length=max_length,
                    generation_text=generation_text,
                    translated_text=translated_text

                )
            else:
                return Response({'error': '(min_length and max_length) > 0 and (max_length < 600)'})
        except Exception as e:
            return Response({'error': f'{e}'})

        value = TextGen.objects.filter(generation_text=generation_text).values()
        return Response({'text': TextGenSerializer(value, many=True).data})


class TranslatorAPIView(generics.ListAPIView):
    serializer_class = TranslatorSerializer

    def get_queryset(self):
        queryset = Translator.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return Response({'error': 'GET-запрос не поддерживается'})

    def post(self, request):
        input = request.data['input']

        translated_text2 = TranslatedText(input).translate_ru()
        text_new = Translator.objects.create(
            input=input,
            translated_text=translated_text2
        )

        value = Translator.objects.filter(translated_text=translated_text2).values()

        return Response({'text': TranslatorSerializer(value, many=True).data})


