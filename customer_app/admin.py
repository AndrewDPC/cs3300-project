from django.contrib import admin
from .models import LegoSet, Review, Member, LegoImages

# Register your models here.
admin.site.register(LegoSet)
admin.site.register(Review)
admin.site.register(Member)
admin.site.register(LegoImages)