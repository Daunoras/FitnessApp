from django import forms

from .models import Workout, Set, Exercise


class WorkoutCreateForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'duration', 'type']
        widgets = {
            'athlete': forms.HiddenInput()
        }


class SetCreateForm(forms.ModelForm):
    class Meta:
        model = Set
        fields = ['exercise', 'weight', 'reps']
        widgets = {
            'workout': forms.HiddenInput()
        }


class ExerciseCreateForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name',
                  'description',
                  'target_muscle',
                  'equipment',
                  'uses_bodyweight']
        widgets = {
            'created_by': forms.HiddenInput()
        }
