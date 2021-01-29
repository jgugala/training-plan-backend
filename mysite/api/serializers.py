from rest_framework import serializers
from .models import Exercise, Training, TrainingItem


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'file']


class TrainingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Training
        fields = ['id', 'name', 'description']


class TrainingItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TrainingItem
        fields = ['id', 'exercise_id', 'training_id', 'position', 'reps_count']
