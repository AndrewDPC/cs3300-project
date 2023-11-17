from django.urls import path, include
from . import views

urlpatterns = [
    
     #Path for the home page 
     path('', views.index, name='index'),

     #Path for browsing LEGO items in a list view.
     path('browse/', views.SetListView.as_view(), name = 'browse'),

     #Path for viewing more details on a specific LEGO set.
     path('set-details/<int:pk>', views.SetDetailView.as_view(), name= 'set-details'),

     #Path for creating a review.
     path('set-details/<int:set_id>/create-review', views.createReview, name= 'create-review'),

     #Path for editing a review.
     path('set-details/<int:set_id>/edit-review/<int:review_id>', views.editReview, name="edit-review"),

     #Path for deleting a review.
     path('set-details/<int:set_id>/delete-review/<int:review_id>', views.deleteReview, name="delete-review"),

     #Path for Django site authentication urls (for login, logout, password management)
     path('accounts/', include('django.contrib.auth.urls')),

     #Path for registering
     path('accounts/register/', views.registerPage, name = 'register-page'),

     #Path for logging out
     path('logout/', views.logoutSuccess, name ='logout')

]
