from django.http import HttpResponse
from django.shortcuts import redirect
from .models import Review

#Decorator for creating, editing, and deleting reviews
def allowedUsers(allowedRoles = []):

    #Takes the view function to override
    def decorator(view_func):

        #Wrapper function to replace the original view function in a way
        def wrapper_func(request, *args, **kwargs):

            group = None

            #Check if user who requested is in a group
            #If they are, get the name of the first group
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            #If they are in the CORRECT group, 
            #Call the original view function
            if group in allowedRoles or request.user.is_staff:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Error: You are not authorized to be on this page.")
            
        return wrapper_func
    
    return decorator

#Decorator for restricting user if they are already logged in
def unauthenticatedUser(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


#Decorator that ensures members can only edit and delete their own reviews
def correctUser(view_func):
    def wrapper_func(request, *args, **kwargs):

        #Get the review object
        reviewId = kwargs.get('review_id')
        review = Review.objects.get(pk=reviewId)

        #Check if logged-in user is author of the review
        if request.user.is_authenticated:
            if review.member.user == request.user:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Error: You are not allowed to edit or delete someone elses review!")
        else:
            return HttpResponse("Error: You are not authorized to be on this page.")
        
    return wrapper_func