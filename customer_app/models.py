from django.db import models
from django.urls import reverse

# Create your models here.

class LegoSet(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length= 400)

    ageRating = models.CharField(max_length=3)
    totalBricks = models.CharField(max_length=4)
    setNumber = models.CharField(max_length=7)
    year = models.CharField(max_length= 4)


    #overallRating = find the average of all ratings
    #review objects (cuz lego sets can have many reviews)

    #Define default String to return the name for representing the Model object."
    def __str__(self):
     return self.title

    #Getting the detailed view
    #def get_absolute_url(self):
    #    return reverse('set-details', args=[str(self.id)])
    