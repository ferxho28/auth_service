from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    phone_number =  models.CharField(max_length=15, blank=True)
        
    REQUIRED_FIELDS = ['email']    
    
    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']

#passwordReset
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def is_valid(self):
           # Token válido por 24 horas
     return (timezone.now() - self.created_at).total_seconds() < 86400