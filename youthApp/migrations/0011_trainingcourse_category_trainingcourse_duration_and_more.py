# Generated by Django 5.1.3 on 2025-05-22 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('youthApp', '0010_userpro_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainingcourse',
            name='category',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='enrollment_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='level',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='trainingcourse',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]
