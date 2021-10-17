from django.db import models
import uuid

from django.db.models import base
from django.contrib.auth.models import AbstractUser

# Create your models here.


class CustomUser(AbstractUser):
    wp_username = models.CharField(max_length=255, blank=False)
    wp_password = models.CharField(max_length=255, blank=False)

    def __str__(self):
        return self.get_full_name()


class Store(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    domain_name = models.CharField(max_length=255, blank=False, unique=True)
    consumer_key = models.CharField(max_length=255, blank=False)
    secret_key = models.CharField(max_length=255, blank=False)
    users = models.ManyToManyField(CustomUser, related_name='stores')

    def __str__(self):
        return self.domain_name
