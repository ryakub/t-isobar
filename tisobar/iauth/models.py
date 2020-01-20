from django.db import models


class VKApp(models.Model):
    client_id = models.IntegerField()
    client_secret = models.CharField(max_length=256)
    scopes = models.CharField(max_length=256)
    display = models.CharField(max_length=256)
    client_secret_key = models.CharField(max_length=256)

    def __str__(self):
        return f"Приложение - {self.client_id}"


class YandexApp(models.Model):
    client_id = models.CharField(max_length=256)
    client_secret = models.CharField(max_length=256)

    def __str__(self):
        return f"Приложение - {self.client_id}"
