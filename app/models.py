from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):

    phone = models.CharField(max_length=15, blank=True, null=True)

    USER_TYPE = (
        ('buyer', 'Buyer'),
        ('agent', 'Agent'),
        ('broker', 'Broker'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE, default='buyer')

    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username