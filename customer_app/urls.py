from django.urls import path
from . import views

urlpatterns = [
    
     path('', views.index, name='index'),

     #Path that leads to the LEGO sets in the browsing, list view
     path('browse/', views.SetListView.as_view(), name = 'browse'),

     #Path that leads to the detailed view of a LEGO set
     
]
