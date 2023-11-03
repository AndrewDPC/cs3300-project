from django.shortcuts import render
from .models import *
from django.views import generic

# Create your views here.

#Home Page
def index(request):
    return render( request, 'customer_app/homepage.html')

#Display of LEGO Sets when browsing
class SetListView(generic.ListView):

    model = LegoSet

#Detailed view of a specific LEGO set
class SetDetailView(generic.DetailView):

    model = LegoSet