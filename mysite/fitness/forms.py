from django import forms
from .models import DayOfEating, Profile, Weighting, Workout, Set, Exercise
from django.contrib.auth.models import User

class DayOfEatingCreateForm(forms.ModelForm):
    class Meta:
        model = DayOfEating
        fields = ['kcal', 'protein', 'date']
        widgets = {'athlete': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if DayOfEating.objects.filter(athlete=self.user, date=date).exists():
            raise forms.ValidationError("You already have an entry for this date.")
        return date

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = []

class WeightingCreateForm(forms.ModelForm):
    class Meta:
        model = Weighting
        fields = ['weight', 'date']
        widgets = {'athlete': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if Weighting.objects.filter(athlete=self.user, date=date).exists():
            raise forms.ValidationError("You already have an entry for this date.")
        return date

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