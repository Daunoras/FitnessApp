from django.contrib.auth.mixins import LoginRequiredMixin

from weighting.services import calculate_bodyweight


def calculate_lift_max(weight, reps, exercise, date, user):
    if exercise.uses_bodyweight:
        bodyweight = calculate_bodyweight(user, date)
        total_weight = int(weight) + bodyweight
        estimated_max = (total_weight * (1 + reps / 30)) - bodyweight
    else:
        estimated_max = (int(weight) * (1 + reps / 30))
    return estimated_max


class AthleteOwnedMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(athlete=self.request.user)


class ExerciseCreatedByMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)
