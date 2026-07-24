from django import forms

from .models import BodyweightGoal, DailyNutritionGoal, LiftingGoal


class BodyweightGoalCreateForm(forms.ModelForm):
    class Meta:
        model = BodyweightGoal
        fields = [
              'start_date',
              'deadline',
              'status',
              'target_bodyweight',
              'start_bodyweight'
        ]
        widgets = {
            'user': forms.HiddenInput()
        }


class DailyNutritionGoalCreateForm(forms.ModelForm):
    class Meta:
        model = DailyNutritionGoal
        fields = [
                'start_date',
                'deadline',
                'status',
                'nutrient_type',
                'amount'
        ]
        widgets = {
            'user': forms.HiddenInput()
        }


class LiftingGoalCreateForm(forms.ModelForm):
    class Meta:
        model = LiftingGoal
        fields = [
            'start_date',
            'deadline',
            'status',
            'exercise',
            'weight',
            'reps',
            'is_estimated'
        ]
        widgets = {
            'user': forms.HiddenInput()
        }
