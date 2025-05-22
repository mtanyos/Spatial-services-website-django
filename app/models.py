from django.db import models
from django.contrib.auth.models import AbstractUser
#from django.contrib.gis.db import models as gis_models

# Create your models here.

class CustomUserDetails(models.Model):
    phone = models.CharField(max_length=9, blank=False, null=True)
    service_type = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=500, null=True)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)  
    longitude = models.FloatField(null=True, blank=True)
    map_photo = models.ImageField(upload_to='location_photos/', null=True, blank=True)
    photo = models.ImageField(upload_to='services_photos/', null=True, blank=True)
    # Add service field directly within CustomUserDetails
    service_name = models.CharField(max_length=100, default='Default Service')  # Adjust the field type as needed

    # Add a ForeignKey field for bookings
    bookings = models.ForeignKey('Booking', on_delete=models.CASCADE, related_name='user_bookings', null=True, blank=True)

    def __str__(self) -> str:
        return self.phone

class Booking(models.Model):
    user_email = models.EmailField()
    user_name = models.CharField(max_length=100)
    booking_time = models.DateTimeField()
    service = models.CharField(max_length=100)  # Adjust the field type as needed

    def __str__(self) -> str:
        return f"{self.user_name}'s booking at {self.booking_time}"


class CustomUserModel(AbstractUser):
    details = models.ForeignKey('CustomUserDetails',on_delete = models.CASCADE,null=True, blank=True)
    def __str__(self) -> str:
        return self.id
    # details = models.OneToOneField(CustomUserDetails, on_delete = models.CASCADE, blank=True)
    # def save(self, *args, **kwargs):
    #     try:
    #         if self.details is None:
    #             self.details = CustomUserDetails.objects.get(pk=1)
    #     except:
    #         self.details = CustomUserDetails.objects.get(pk=1)
    #    super(CustomUserModel, self).save(*args, **kwargs)
