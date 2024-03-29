# Generated by Django 3.1.5 on 2021-11-09 16:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0002_auto_20210120_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='training',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='trainingitem',
            name='exercise',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_items', to='api.exercise'),
        ),
        migrations.AlterField(
            model_name='trainingitem',
            name='training',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_items', to='api.training'),
        ),
    ]
