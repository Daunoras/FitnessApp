from django.db import models
from polymorphic.models import PolymorphicModel
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from weighting.models import Weighting


class GoalStatus(models.TextChoices):
    ACTIVE = "Active", "active"
    COMPLETED = "Completed", "completed"
    INACTIVE = "Inactive", "inactive"
    CANCELED = "Canceled", "canceled"
    FAILED = "Failed", "failed"


class Goal(PolymorphicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    start_date = models.DateField(
        "Starting date",
                    blank=False,
                    null=False,
                    help_text="The date of the goal start")
    deadline = models.DateField("Deadline", blank=True, null=True)
    status = models.CharField(
        "Status",
                    max_length=10,
                    null=False,
                    blank=False,
                    choices=GoalStatus.choices,
                    default=GoalStatus.INACTIVE
    )

    def clean(self):
        super().clean()

        if self.status not in GoalStatus.values:
            raise ValidationError({
                "Goal status": (
                    f"Invalid goal status: {self.status}"
                )
            })


class BodyweightGoal(Goal):
    target_bodyweight = models.FloatField("Target bodyweight", blank=False, null=False)
    start_bodyweight = models.FloatField("Bodyweight at start", blank=False, null=False)
    is_weight_loss = models.BooleanField("Is the goal for weight loss", blank=False, null=False)

    def complete_goal(self):
        self.status = GoalStatus.COMPLETED

    def check_completeness(self):
        current_weight = Weighting.objects.filter(athlete=self.user).order_by("-date").first().weight
        if ((not self.is_weight_loss and current_weight >= self.target_bodyweight)
             or (self.is_weight_loss and current_weight <= self.target_bodyweight)):
            return True
        else:
            return False

    def progress_percentage(self):
        current_weight = Weighting.objects.filter(athlete=self.user).order_by("-date").first().weight
        if self.is_weight_loss:
            progress = self.start_bodyweight - current_weight / self.start_bodyweight - self.target_bodyweight
        else:
            progress = current_weight - self.start_bodyweight / self.target_bodyweight - self.start_bodyweight
        return progress

