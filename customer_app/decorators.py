from django.http import HttpResponse
from django.shortcuts import redirect

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
            if group in allowedRoles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse("Bad")
            
        return wrapper_func
    
    return decorator