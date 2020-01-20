from django.contrib import admin
from iYandex import models

admin.site.register(models.YandexConnection)
admin.site.register(models.YandexMetrikaClient)
admin.site.register(models.YandexDirectClient)
