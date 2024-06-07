from django import forms
from .models import DayOfEating


class DateInput(forms.DateInput):
    input_type = 'date'

class DayOfEatingCreateForm(forms.ModelForm):
    class Meta:
        model = DayOfEating
        fields = ['kcal', 'protein']
        widgets = {'athlete': forms.HiddenInput(), 'date': DateInput()}