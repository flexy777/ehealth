# Generated by Django 4.2.6 on 2023-10-28 11:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('health_app', '0002_medicalrecord_disease'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='is_health_worker',
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('patient', 'Patient'), ('health_worker', 'Health Worker')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
