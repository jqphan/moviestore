from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Petition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="petitions")
    created_at = models.DateTimeField(auto_now_add=True)
    is_open = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    @property
    def yes_count(self):
        return self.votes.filter(choice=Vote.CHOICE_YES).count()
    
class Vote(models.Model):
    CHOICE_YES = "YES"
    CHOICES = [(CHOICE_YES, "Yes")]

    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name = "votes")
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="petition_votes")
    choice = models.CharField(max_length=3, choices=CHOICES, default=CHOICE_YES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["petition", "voter"], name="unique_vote_per_user_per_petition")
        ]

    def __str__(self):
        return f"{self.voter} -> {self.petition} ({self.choice})"