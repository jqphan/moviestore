from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Petition, Vote
admin.site.register(Petition)
admin.site.register(Vote)