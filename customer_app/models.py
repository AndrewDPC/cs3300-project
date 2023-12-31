from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

#Class for LEGO sets
class LegoSet(models.Model):

    #Title and description of the set 
    title = models.CharField(max_length=100)
    description = models.TextField(max_length= 600)

    #Some important information to include for a LEGO set 
    thumbnail = models.ImageField(blank=True)
    ageRating = models.CharField(max_length=3)
    setNumber = models.CharField(max_length=7)
    totalBrickCount = models.CharField(max_length=4)
    minifigureCount = models.CharField(max_length= 2, default=0)
    yearReleased = models.CharField(max_length= 4)

    #Review related properties
    satisfactionRating = models.IntegerField(default=0)
    reviewCount = models.IntegerField(default=0)

    #Define default String to return the name for representing the Model object.
    def __str__(self):
        return self.title

    #Generate the right link using the unique set ID from database
    def get_absolute_url(self):
        return reverse('set-details', args=[str(self.id)])
    
    #Method that is called everytime a review is added or deleted to a LEGO set
    #Makes sure to update the LEGO set's satisfaction rating
    def updateSatisfactionRating(self):

        #Gets all the reviews associated with this set
        reviews = self.review_set.all()

        #Calculates the total ratings using the numbers that each review gave
        total_rating = sum(review.rating for review in reviews)

        #If there are reviews, then calculate the satisfaction rating
        #Else, the satisfaction rating is 0
        if reviews:
            self.satisfactionRating = (total_rating / (len(reviews) * 5) ) * 100
            
        else:
            self.satisfactionRating = 0

        #Save model instance to database
        self.save()

    #Method that increments the review count variable everytime one is added
    def incrementReviews(self):
        self.reviewCount += 1
        self.save()

    #Method that decrements the review count variable everytime one is removed
    def decrementViews(self):
        if self.reviewCount != 0:
            self.reviewCount -= 1
            self.save()


#Class for LEGO set images
class LegoImages(models.Model):
    legoSet = models.ForeignKey(LegoSet,on_delete=models.CASCADE)
    image = models.ImageField()
    imageTitle = models.CharField(max_length= 30,default= "")

    #Define default String to return the name for representing the Model object.
    def __str__(self):
        return self.imageTitle

#Class for a logged in user
class Member(models.Model):

    #Fields to differentiate a user 
    userName = models.CharField(max_length= 50)
    firstName = models.CharField(max_length= 50, default="")
    lastName = models.CharField(max_length= 50, default="")

    #bio = models.TextField(max_length= 200)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    #One to one relationship
    user = models.OneToOneField(User, null= True, on_delete=models.CASCADE)

    def __str__(self):
        return self.userName
    
#Class for user reviews
class Review(models.Model):

   #Fields for the title, opinion, and rating they choose to give
   #Author
   title = models.CharField(max_length=50)
   opinion = models.TextField(max_length= 400)
   rating = models.IntegerField(default = 0)
   dateCreated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

   #Create relationship to specific LEGO set
   legoSet = models.ForeignKey(LegoSet, on_delete=models.CASCADE)
   member = models.ForeignKey(Member, null=True, on_delete=models.CASCADE)

   #Define default String to return the name for representing the Model object.
   def __str__(self):
      return self.title
   
   #Method that is called everytime a review is created or deleted
   #Overriding the 'save' method
   def save(self, *args, **kwargs):
        
        #Since the save method is used for creating and changing an object, have to check if review is new or not
        isNewReview = self._state.adding  

        #Call the default save method first 
        super(Review, self).save(*args, **kwargs)

        #Update the satisfaction rating for the LEGO set
        self.legoSet.updateSatisfactionRating()  

        #If it's a new review, then increment total reviews for the LEGO set
        if isNewReview:
            self.legoSet.incrementReviews()  

   #Method that is called everytime a review is deleted
   #overriding the 'delete' method
   def delete(self, *args, **kwargs):
        
        #Get the LEGO set
        legoSet = self.legoSet

        #Call the default delete method first
        super(Review, self).delete(*args, **kwargs)

        #Update the satisfaction rating and decrement the total reviews for a LEGO set 
        legoSet.updateSatisfactionRating()  
        legoSet.decrementViews()  
