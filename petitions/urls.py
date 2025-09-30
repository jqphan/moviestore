from django.urls import path
from . import views

app_name = "petitions"

urlpatterns = [
    path("", views.PetitionListView.as_view(), name="list"),
    path("new/", views.PetitionCreateView.as_view(), name="create"),
    path("<int:pk>/", views.PetitionDetailView.as_view(), name="detail"),
    path("<int:pk>/vote-yes/", views.vote_yes, name="vote_yes"),
]