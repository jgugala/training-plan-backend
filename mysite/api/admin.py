from django.contrib import admin

# Register your models here.
from .models import Exercise, Training, TrainingItem

admin.site.register(Exercise)
admin.site.register(Training)
admin.site.register(TrainingItem)

