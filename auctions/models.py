from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import ModelState
from django.core.validators import MinValueValidator
from django.db.models.fields.related import OneToOneField

class User(AbstractUser):
    pass


class listing(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    desc=models.TextField()
    price = models.IntegerField()
    url = models.URLField()
    category=models.CharField(blank = True, max_length=64)
    date = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
   
    
    def __str__(self):
        return f"TITLE:--{self.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, blank=False)
    listing=models.ForeignKey(listing,on_delete=models.CASCADE,blank=False)

    def __str__(self):
        return f"USER:{self.user}--TITLE:{self.listing.title}"

class comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    

    def __str__(self):
        return f"{self.user}---{self.content}--{self.listing }"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(listing, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.user}--{self.listing}---{self.price}$"