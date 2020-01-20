from django.db import models
from django.contrib.auth.models import User


class VKConnection(models.Model):
    access_token = models.CharField(max_length=356)
    vk_first_name = models.CharField(max_length=256)
    vk_last_name = models.CharField(max_length=256)
    vk_user_id = models.IntegerField()
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.vk_first_name} {self.vk_last_name}"


class VKClient(models.Model):
    access_token = models.CharField(max_length=356)
    vk_client_name = models.CharField(max_length=256)
    vk_client_id = models.IntegerField()
    vk_account_name = models.CharField(max_length=256)
    vk_account_id = models.IntegerField()
    vk_page = models.CharField(max_length=256)
    vk_page_access_token = models.CharField(max_length=356)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(VKConnection, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.vk_client_name}"
