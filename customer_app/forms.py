from django.forms import ModelForm
from .models import Review

#Creating a Review form with said fields.
class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ('title', 'opinion', 'rating')