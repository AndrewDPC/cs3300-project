from django.shortcuts import render

# Create your views here.

#Home Page
def index(request):
    return render( request, 'customer_app/homepage.html')
