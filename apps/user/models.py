from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_image/', blank=True, null=True)
    phone_number = models.CharField(max_length=25, blank=True, null=True)
    date_of_birth= models.DateField(blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.username