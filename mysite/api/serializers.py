import pdb

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _
from rest_framework import serializers

from .models import Exercise, Training, TrainingItem


# Exercise Serializer
class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'file']


# Training Item Serializer
class TrainingItemSerializer(serializers.ModelSerializer):
    exercise_id = serializers.PrimaryKeyRelatedField(queryset=Exercise.objects.all(), source='exercise')
    training_id = serializers.PrimaryKeyRelatedField(queryset=Training.objects.all(), source='training')

    class Meta:
        model = TrainingItem
        fields = ['id', 'exercise_id', 'training_id', 'position', 'reps_count']


# Training Item Serializer (reduced version for the Training Serializer embedding purposes)
class NestedTrainingItemSerializer(TrainingItemSerializer):
    # https://bit.ly/3wETrbc
    # https://bit.ly/3DaQ6De
    id = serializers.IntegerField(required=False)

    class Meta:
        model = TrainingItem
        fields = [field for field in TrainingItemSerializer.Meta.fields if field != 'training_id']


# Training Serializer
# https://www.django-rest-framework.org/api-guide/serializers/#saving-instances
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
                pdb.set_trace()
                training_item['id'] = None
                TrainingItem.objects.create(training=training, **training_item)

        return training

    def update(self, instance, validated_data):
        training_items = validated_data.pop('training_items', None)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)

        if training_items is not None:
            # pdb.set_trace()
            for training_item in training_items:
                training_item_id = training_item.get('id', None)
                if training_item_id is None:
                    TrainingItem.objects.create(training=instance, **training_item)
                else:
                    try:
                        training_item_for_update = TrainingItem.objects.get(id=training_item_id, training=instance)
                    except ObjectDoesNotExist:
                        message = _('Invalid training item pk "' + str(training_item_id) + '" - object does not exist.')
                        raise serializers.ValidationError(message, code='invalid_id')
                    training_item_for_update.position = training_item.get('position', training_item_for_update.position)
                    training_item_for_update.reps_count = \
                        training_item.get('reps_count', training_item_for_update.reps_count)
                    training_item_for_update.exercise = \
                        training_item.get('exercise', training_item_for_update.exercise)
                    # pdb.set_trace()
                    training_item_for_update.save()

        # model save method (not the serializer one) - saving to the db
        instance.save()
        return instance


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        # There is also a shortcut allowing you to specify arbitrary additional keyword arguments on fields,
        # using the extra_kwargs option. As in the case of read_only_fields, this means you do not need to explicitly
        # declare the field on the serializer.
        # https://www.django-rest-framework.org/api-guide/serializers/#additional-keyword-arguments
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'],
            validated_data['email'],
            validated_data['password']
        )

        return user


# Login Serializer
class LoginSerializer(serializers.ModelSerializer):
    pass
