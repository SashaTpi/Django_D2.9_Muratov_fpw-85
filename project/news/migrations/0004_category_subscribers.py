# Generated by Django 3.2.16 on 2022-11-15 11:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0003_auto_20221102_2121'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='subscribers',
            field=models.ManyToManyField(blank=True, related_name='subscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]
