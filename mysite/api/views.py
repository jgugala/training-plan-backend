from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ExerciseSerializer, TrainingSerializer, TrainingItemSerializer
from .models import Exercise, Training, TrainingItem


# Create your views here.


class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all().order_by('id')
    serializer_class = ExerciseSerializer


class TrainingViewSet(viewsets.ModelViewSet):
    queryset = Training.objects.all().order_by('id')
    serializer_class = TrainingSerializer


class TrainingItemViewSet(viewsets.ModelViewSet):
    queryset = TrainingItem.objects.all().order_by('id')
    serializer_class = TrainingItemSerializer
