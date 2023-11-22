from django.forms import ModelForm
from .models import Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#Creating a Review form with said fields.
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'opinion')


#Creating a user registration form with said fields
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2'] 
      
