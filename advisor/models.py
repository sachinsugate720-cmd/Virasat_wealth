from django.db import models
from django.contrib.auth.models import User


class ConsultationRequest(models.Model):
    GOAL_RETIREMENT = "retirement"
    GOAL_WEALTH = "wealth_creation"
    GOAL_CHILD = "child_education"
    GOAL_TAX = "tax_saving"

    GOAL_CHOICES = [
        (GOAL_RETIREMENT, "Retirement"),
        (GOAL_WEALTH, "Wealth Creation"),
        (GOAL_CHILD, "Child Education"),
        (GOAL_TAX, "Tax Saving"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="consultation_requests"
    )
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    primary_goal = models.CharField(max_length=32, choices=GOAL_CHOICES)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} ({self.get_primary_goal_display()})"
