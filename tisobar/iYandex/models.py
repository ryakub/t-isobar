from django.db import models
from django.contrib.auth.models import User


class YandexConnection(models.Model):
    access_token = models.CharField(max_length=356)
    ya_first_name = models.CharField(max_length=256)
    ya_last_name = models.CharField(max_length=256)
    ya_user_id = models.IntegerField()
    ya_email = models.EmailField()
    ya_login = models.CharField(max_length=256)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ya_first_name} {self.ya_last_name} {self.ya_login}"


class YandexDirectClient(models.Model):
    access_token = models.CharField(max_length=356)
    ya_client_login = models.CharField(max_length=256)
    ya_client_id = models.IntegerField()
    ya_agency_login = models.CharField(max_length=256, null=True)
    ya_agency_id = models.IntegerField(null=True)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(YandexConnection, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ya_client_login}"


class YandexMetrikaClient(models.Model):
    access_token = models.CharField(max_length=356)
    ya_login = models.CharField(max_length=256)
    ya_id = models.IntegerField()
    ya_metrika_id = models.IntegerField()
    ya_metrika_name = models.CharField(max_length=256)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(YandexConnection, on_delete=models.CASCADE)
    direct = models.ForeignKey(YandexDirectClient, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.ya_metrika_name} - {self.ya_metrika_id}"
