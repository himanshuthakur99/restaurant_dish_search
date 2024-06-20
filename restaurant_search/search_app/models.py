from django.db import models

class Dish(models.Model):
    name = models.CharField(max_length=255)
    restaurant_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    items = models.TextField()
    prices = models.TextField(default='{}')  
    rating = models.FloatField(default=0)  

    def __str__(self):
        return self.name

