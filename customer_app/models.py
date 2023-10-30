from django.db import models

# Create your models here.

class LegoSet(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length= 400)

    ageRating = models.CharField(max_length=3)
    totalBricks = models.CharField(max_length=4)
    setNumber = models.CharField(max_length=7)
    year = models.CharField(max_length= 4)
    
    #rating = find the average of all ratings
    #review objects (cuz lego sets can have many reviews)