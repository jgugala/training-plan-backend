from rest_framework import serializers
from .models import Exercise, Training, TrainingItem


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'file']


class TrainingItemSerializer(serializers.ModelSerializer):
    exercise_id = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), source='exercise')
    training_id = serializers.PrimaryKeyRelatedField(queryset=Training.objects.all(), source='training')

    class Meta:
        model = TrainingItem
        fields = ['id', 'exercise_id', 'training_id', 'position', 'reps_count']


class NestedTrainingItemSerializer(TrainingItemSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = TrainingItem
        fields = [field for field in TrainingItemSerializer.Meta.fields if field != 'training_id']


class TrainingSerializer(serializers.ModelSerializer):
    training_items = NestedTrainingItemSerializer(many=True, required=False)

    class Meta:
        model = Training
        fields = ['id', 'name', 'description', 'training_items']

    def create(self, validated_data):
        training_items = validated_data.pop('training_items', None)
        training = Training.objects.create(**validated_data)
        if training_items is not None:
            for training_item in training_items:
                TrainingItem.objects.create(training=training, **training_item)

        return training

    def update(self, instance, validated_data):
        training_items = validated_data.pop('training_items', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        if training_items is not None:
            for training_item in training_items:
                training_item_id = training_item.get('id', None)
                if training_item_id is None:
                    TrainingItem.objects.create(training=instance, **training_item)
                else:
                    training_item_for_update = TrainingItem.objects.get(id=training_item_id, training=instance)
                    training_item_for_update.position = training_item.get('position', training_item_for_update.position)
                    training_item_for_update.reps_count = \
                        training_item.get('reps_count', training_item_for_update.reps_count)
                    training_item_for_update.save()

        instance.save()
        return instance
