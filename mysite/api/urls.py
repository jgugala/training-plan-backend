from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'exercises', views.ExerciseViewSet)
router.register(r'trainings', views.TrainingViewSet)
router.register(r'training_items', views.TrainingItemViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # ...
    # Route TemplateView to serve Swagger UI template.
    #   * Provide `extra_context` with view name of `SchemaView`.
    path('swagger/', TemplateView.as_view(template_name='swagger-ui.html'), name='swagger_ui'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
