from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser): # model user
    class AuthProvider(models.TextChoices): #enum
        LOCAL = "local", "local"
        GOOGLE = "google", "google"

    #column    
    max_song = models.IntegerField(default=20)
    auth_provider = models.CharField(max_length=6, choices=AuthProvider.choices, default=AuthProvider.LOCAL)

    class Meta:
        db_table = "user"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
