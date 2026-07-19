from django import forms
from .models import BodyweightGoal


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
        widgets = {'user': forms.HiddenInput()}