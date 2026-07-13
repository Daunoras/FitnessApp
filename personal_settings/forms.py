from django import forms
from .models import ExerciseChoices, PersonalSettings


class PersonalSettingsForm(forms.ModelForm):
    exercise_pool = forms.MultipleChoiceField(
                choices=ExerciseChoices.choices,
                widget=forms.CheckboxSelectMultiple,
                required=False
    )

    class Meta:
        model = PersonalSettings
        fields = ["exercise_pool"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["exercise_pool"].initial = (
                self.instance.exercise_pool
            )