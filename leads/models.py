from django.db import models
from services.models import Service

class Lead(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    # Link to the Service model so you know what they want
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True) 
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.service}"