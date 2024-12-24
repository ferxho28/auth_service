from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    firts = models.TextField(null=False)
    email = models.EmailField(unique=True, null=False)
    password = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    phone_number =  models.CharField(max_length=15, blank=True)
        
    REQUIRED_FIELDS = ['email']    
    
    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']