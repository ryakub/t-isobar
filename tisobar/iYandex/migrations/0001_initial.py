# Generated by Django 3.0.2 on 2020-01-19 20:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='YandexApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_id', models.CharField(max_length=256)),
                ('client_secret', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='YandexConnection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=356)),
                ('ya_first_name', models.CharField(max_length=256)),
                ('ya_last_name', models.CharField(max_length=256)),
                ('ya_user_id', models.IntegerField()),
                ('ya_email', models.EmailField(max_length=254)),
                ('ya_login', models.CharField(max_length=256)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
