from django import forms
from .models import Workout, Set


class WorkoutCreateForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'duration', 'type']
        widgets = {'athlete': forms.HiddenInput()}


class SetCreateForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['exercise', 'weight', 'reps']
        widgets = {
            'workout': forms.HiddenInput()
        }