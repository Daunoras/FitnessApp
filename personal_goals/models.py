import datetime

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from polymorphic.models import PolymorphicModel

from fitness.models import Exercise
from nutrition.models import DayOfEating
from weighting.models import Weighting


class GoalStatus(models.TextChoices):
    ACTIVE = "Active", "active"
    COMPLETED = "Completed", "completed"
    INACTIVE = "Inactive", "inactive"
    CANCELED = "Canceled", "canceled"
    FAILED = "Failed", "failed"


class NutrientType(models.TextChoices):
    CALORIES = "Calories", "calories"
    PROTEIN = "Protein", "protein"
    CARBOHYDRATES = "Carbohydrates", "carbohydrates"
    FATS = "Fats", "fats"


class Goal(PolymorphicModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    start_date = models.DateField(
        "Starting date",
        blank=False,
        null=False,
        help_text="The date of the goal start"
    )
    end_date = models.DateField("End date", blank=True, null=True)
    deadline = models.DateField("Deadline", blank=True, null=True)
    status = models.CharField(
        "Status",
        max_length=10,
        null=False,
        blank=False,
        choices=GoalStatus.choices,
        default=GoalStatus.INACTIVE
    )
    detail_url_name = None

    def get_detail_view_url_name(self):
        return reverse(self.detail_url_name, kwargs={"pk": self.pk})

    def clean(self):
        super().clean()

        if self.status not in GoalStatus.values:
            raise ValidationError({
                "Goal status": (
                    f"Invalid goal status: {self.status}"
                )
            })

    def complete_goal(self):
        self.status = GoalStatus.COMPLETED
        self.end_date = datetime.date.today()


class BodyweightGoal(Goal):
    target_bodyweight = models.FloatField("Target bodyweight", blank=False, null=False)
    start_bodyweight = models.FloatField("Bodyweight at start", blank=False, null=False)
    is_weight_loss = models.BooleanField("Is the goal for weight loss", blank=False, null=False)
    detail_url_name = "bodyweight-goal-details"

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

    def save(self, *args, **kwargs):
        if not self.is_weight_loss:
            if self.start_bodyweight > self.target_bodyweight:
                self.is_weight_loss = True
            else:
                self.is_weight_loss = False
        super().save(*args, **kwargs)

    def __str__(self):
        description = f"Bodyweight {self.start_bodyweight}-{self.target_bodyweight}"
        if self.deadline:
            description += f" to {self.deadline}"
        return description


class DailyNutritionGoal(Goal):
    amount = models.FloatField("Consumed amount", blank=False, null=False)
    nutrient_type = models.CharField(
        "Nutrient type",
        max_length=14,
        null=False,
        blank=False,
        choices=NutrientType.choices
    )
    detail_url_name = "nutrition-goal-details"

    def progress_percentage(self):
        todays_eating = DayOfEating.objects.filter(
            athlete=self.user, date=datetime.date.today()
        ).order_by("-date").first()
        progress = 0
        if todays_eating:
            if self.nutrient_type == NutrientType.CALORIES:
                progress = todays_eating.kcal / self.amount
            elif self.nutrient_type == NutrientType.PROTEIN:
                progress = todays_eating.protein / self.amount
        return progress

    def __str__(self):
        return f"Daily {self.nutrient_type} goal {self.amount}"


class LiftingGoal(Goal):
    weight = models.FloatField("Weight", blank=False, null=False)
    reps = models.IntegerField("Reps", blank=False, null=False)
    exercise = models.ForeignKey(Exercise, on_delete=models.SET_NULL, blank=True, null=True)
    is_estimated = models.BooleanField("Estimated", blank=False, null=False)
    detail_url_name = "lifting-goal-details"

    def __str__(self):
        return f"{self.exercise} {self.weight}kg for {self.reps} reps"
