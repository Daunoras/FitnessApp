from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings


class ExerciseChoices(models.TextChoices):
    CUSTOM = "Custom", "custom"
    DEFAULT = "Default", "default"
    EVERYONE = "Everyone", "everyone"


class PersonalSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="settings")
    exercise_pool = models.JSONField(default=list)

    def clean(self):
        super().clean()

        allowed = set(ExerciseChoices.values)
        invalid = set(self.exercise_pool) - allowed

        if invalid:
            raise ValidationError({
                "exercise_pool": (
                    f"Invalid exercise pool options: {', '.join(invalid)}"
                )
            })
