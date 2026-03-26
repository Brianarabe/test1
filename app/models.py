from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


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
    
class Property(models.Model):

    PROPERTY_TYPE = [
        ('house_lot', 'House and Lot'),
    ]

    LISTING_STATUS = [
        ('sale', 'For Sale'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()

    property_type = models.CharField(
        max_length=20,
        choices=PROPERTY_TYPE,
        default='house_lot'
    )

    listing_status = models.CharField(
        max_length=10,
        choices=LISTING_STATUS,
        default='sale'
    )

    price = models.DecimalField(max_digits=12, decimal_places=2)

    location = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    province = models.CharField(max_length=100)

    bedrooms = models.IntegerField()
    bathrooms = models.IntegerField()

    floor_area = models.DecimalField(max_digits=10, decimal_places=2)
    lot_area = models.DecimalField(max_digits=10, decimal_places=2)

    parking_spaces = models.IntegerField(default=0)

    image = models.ImageField(upload_to='property_images/', blank=True, null=True)

    agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to='property_images/')

    def __str__(self):
        return f"Image for {self.property.title}"