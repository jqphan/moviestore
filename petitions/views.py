from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.contrib import messages

from .models import Petition, Vote
from .forms import PetitionForm

class PetitionListView(ListView):
    model = Petition
    template_name = "petitions/list.html"
    context_object_name = "petitions"

    def get_queryset(self):
        # Annotate YES counts for faster list display
        return (
            Petition.objects
            .annotate(yes_count_anno=Count("votes", filter=Q(votes__choice=Vote.CHOICE_YES)))
            .order_by("-created_at")
        )

class PetitionCreateView(LoginRequiredMixin, CreateView):
    model = Petition
    form_class = PetitionForm
    template_name = "petitions/create.html"
    success_url = reverse_lazy("petitions:list")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "Petition created.")
        return super().form_valid(form)

class PetitionDetailView(DetailView):
    model = Petition
    template_name = "petitions/detail.html"
    context_object_name = "petition"

@login_required
def vote_yes(request, pk):
    petition = get_object_or_404(Petition, pk=pk, is_open=True)
    if request.method != "POST":
        return redirect("petitions:detail", pk=pk)

    vote, created = Vote.objects.get_or_create(
        petition=petition, voter=request.user, defaults={"choice": Vote.CHOICE_YES}
    )
    if created:
        messages.success(request, "Thanks! Your YES vote was recorded.")
    else:
        messages.info(request, "You already voted YES on this petition.")
    return redirect("petitions:detail", pk=pk)