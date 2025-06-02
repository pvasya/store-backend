from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_blacklisted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.username

class Goods(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.URLField()
    buyers = models.ManyToManyField(User, related_name='purchases', blank=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Goods'
