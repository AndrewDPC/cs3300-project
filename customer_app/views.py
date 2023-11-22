from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views import generic
from .forms import ReviewForm, CreateUserForm
from .decorators import *

# Create your views here.

#View for the home page
def index(request):
    return render( request, 'customer_app/homepage.html')

#View for displaying LEGO sets in the browse section
class SetListView(generic.ListView):

    model = LegoSet


#Detailed view for a specific LEGO set 
class SetDetailView(generic.DetailView):

    model = LegoSet

    #Override the method so more data can be passed
    def get_context_data(self, **kwargs):

        #Call the base implementation first to get the context
        context = super().get_context_data(**kwargs)

        #Get all reviews associated with the LEGO set (query)
        #context['reviews'] = Review.objects.filter(legoSet=self.object)

        #Get all images associated with the LEGO set
        context['setImages'] = LegoImages.objects.filter(legoSet=self.object)

        #Check if admin is logged in or not
        if(not self.request.user.is_staff and not self.request.user.is_anonymous):
            #Get the current user's member instance
            member = Member.objects.get(user=self.request.user)

            #Get all reviews associated with the LEGO set and the current member
            context['memberReviews'] = Review.objects.filter(legoSet=self.object, member=member)

            #Get all reviews associated with the LEGO set that excludes the current member
            context['otherReviews'] = Review.objects.filter(legoSet=self.object).exclude(member=member)
        else:
            #Get all reviews associated with the LEGO set
            context['otherReviews'] = Review.objects.filter(legoSet=self.object)
        
        #Get all the reviews. Used for math
        context['allReviews'] = Review.objects.filter(legoSet=self.object)

        #If there are reviews, then calculate stuff
        if context['allReviews']:

            #Get the sum of user ratings
            totalStars = sum(review.rating for review in context['allReviews'])
            context['totalStars'] = totalStars

            #Get how many actual stars there are for a set 
            #(EX: If there are two reviews for a set, there should be 10 actual stars since each review can give a max of 5 stars)
            actualStars = 0
            for review in context['allReviews']:
                actualStars += 5
            context['actualStars'] = actualStars

            
            #Get the overall rating in number form. (5-star rating system)
            context['overallRatingNum'] = (totalStars/actualStars) * 5


        return context

      
#View for creating a review
@allowedUsers(allowedRoles = ['member'])
def createReview(request, set_id):

    #Set the form
    form = ReviewForm()
    #Get the correct LEGO set using the correct ID
    legoSet = LegoSet.objects.get(pk=set_id)

    #Check if POST method was requested
    if request.method == 'POST':

        #Create a copy of the POST data
        review_data = request.POST.copy()

        #Associates with the correct LEGO set using the correct ID
        review_data['set_id'] = set_id

        #Create a new form with the review data
        form = ReviewForm(review_data)

        #Sees if the form is valid and if the rating is not 0. If so, then save it
        if form.is_valid() and int(request.POST.get('rating', 0)) != 0:

            # Save the form without committing to the database
            review = form.save(commit=False)

            # Set the review relationship
            review.legoSet = legoSet

            #Associate member with the review
            review.member = request.user.member

            #Assign the rating from the POST data
            review.rating = int(request.POST.get('rating', 0))

            #Now save it to the database
            review.save()

            #Redirect back to the detailed page for a LEGO set
            return redirect('set-details', set_id)
        else:
            messages.error(request, "You forgot to rate the set!")
                

    #Send correct data to the form and set id for page redirection
    context = {'form': form, 'legoSetId': set_id}
    return render(request, 'customer_app/review_form.html', context)


#View for editing a review
@correctUser
def editReview(request, review_id):

    #Get the correct review
    review = Review.objects.get(id=review_id)

    #Get the correct set. Will be used for page redirection
    legoSet = review.legoSet.id

    #Populate the form with pre-existing information
    form = ReviewForm(instance = review)

    #Check if POST method was requested
    if request.method == 'POST':

        #Creates the form instance with updated data and the pre-existing review
        form = ReviewForm(request.POST, instance = review)

        #Validation of form
        if(form.is_valid):

            #Assign the rating from the POST data
            review.rating = int(request.POST.get('rating', 0))
            #Now save it to the database
            review.save()

            #Save the form
            form.save()

            #Redirect back to the detailed page for a LEGO set
            return redirect('set-details', legoSet)
    
    #Send correct data to the form and set id for page redirection
    context = {'form': form, 'legoSetId':legoSet}
    return render(request, 'customer_app/review_form.html', context)

#View for deleting a review
@correctUser
def deleteReview(request, review_id):

    #Get the correct review
    review = Review.objects.get(id=review_id)

    #Get the correct set. Will be used for page redirection
    legoSet = review.legoSet.id

    #Delete review from the database
    review.delete()

    #Redirect back to the detailed page for a LEGO set
    return redirect('set-details', legoSet)


#View for registering a user
@unauthenticatedUser
def registerPage(request):

    form = CreateUserForm()

    if request.method =='POST':
            
        form = CreateUserForm(request.POST)

        if form.is_valid():

            #Save form to database and store the instance in variable
            user = form.save()

            #Get the all fields from the form
            username = form.cleaned_data.get('username')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            #Get the correct group
            group = Group.objects.get(name='member')

            #Add the user to the correct group
            user.groups.add(group)

            #Create the member object and associate with user
            Member.objects.create(

                user=user,
                userName = username,
                firstName = first_name,
                lastName = last_name,
            )

            #Create success message 
            messages.success(request, 'Account was created for ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'registration/register.html', context)

#View for the logging out
@login_required(login_url='login')
def logoutSuccess(request):
    logout(request)
    return render( request, 'registration/logout.html')
