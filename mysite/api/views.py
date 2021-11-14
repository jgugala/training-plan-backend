from knox.models import AuthToken
from rest_framework import viewsets, permissions, generics
from rest_framework.response import Response

from .models import Exercise, TrainingItem
from .serializers import ExerciseSerializer, TrainingSerializer, TrainingItemSerializer, RegisterSerializer, \
    UserSerializer


# Create your views here.

# Exercise ViewSet
class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all().order_by('id')
    serializer_class = ExerciseSerializer


# Training ViewSet
class TrainingViewSet(viewsets.ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = TrainingSerializer

    def get_queryset(self):
        return self.request.user.trainings.all().order_by('id')

    # The user isn't sent as part of the serialized representation, but is instead a property of the incoming
    # request. The way we deal with that is by overriding a .perform_create() method on our snippet views,
    # that allows us to modify how the instance save is managed, and handle any information that is implicit in the
    # incoming request or requested URL. These hooks are particularly useful for setting attributes that are implicit
    # in the request, but are not part of the request data. For instance, you might set an attribute on the object
    # based on the request user, or based on a URL keyword argument.
    # https://www.django-rest-framework.org/tutorial/4-authentication-and-permissions/#associating-snippets-with-users
    def perform_create(self, serializer):
        # Sometimes you'll want your view code to be able to inject additional data at the point of saving the
        # instance. This additional data might include information like the current user, the current time,
        # or anything else that is not part of the request data.
        # https://www.django-rest-framework.org/api-guide/serializers/#passing-additional-attributes-to-save
        serializer.save(owner=self.request.user)


# TrainingItem ViewSet
class TrainingItemViewSet(viewsets.ModelViewSet):
    queryset = TrainingItem.objects.all().order_by('id')
    serializer_class = TrainingItemSerializer


# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # The .is_valid() method takes an optional raise_exception flag that will cause it to raise a
        # serializers.ValidationError exception if there are validation errors.
        # https://www.django-rest-framework.org/api-guide/serializers/#raising-an-exception-on-invalid-data
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            # There are some cases where you need to provide extra context to the serializer in addition to the
            # object being serialized. One common case is if you're using a serializer that includes hyperlinked
            # relations, which requires the serializer to have access to the current request so that it can properly
            # generate fully qualified URLs. You can provide arbitrary additional context by passing a context
            # argument when instantiating the serializer.
            # https://www.django-rest-framework.org/api-guide/serializers/#including-extra-context
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
            'token': AuthToken.objects.create(user)[1]
        })

