from django.db import models
from positions import PositionField

# Create your models here.


class BaseModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created_at`` and ``updated_at`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Exercise(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    file = models.FileField(blank=True)

    def __str__(self):
        return self.name


class Training(BaseModel):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class TrainingItem(BaseModel):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    position = PositionField(collection='training')
    reps_count = models.IntegerField()

    class Meta:
        ordering = ['training', 'position']
