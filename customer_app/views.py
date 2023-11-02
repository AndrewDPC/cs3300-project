from django.shortcuts import render
from .models import *
from django.views import generic

# Create your views here.

#Home Page
def index(request):
    return render( request, 'customer_app/homepage.html')

#Display of Lego Sets when browsing
class SetListView(generic.ListView):

    model = LegoSet
