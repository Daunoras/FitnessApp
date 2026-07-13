from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from .models import PersonalSettings
from .forms import PersonalSettingsForm
from django.urls import reverse_lazy
from .services import get_personal_settings


class PersonalSettingsView(LoginRequiredMixin, UpdateView):
    model = PersonalSettings
    form_class = PersonalSettingsForm
    template_name = 'personal_settings.html'
    success_url = reverse_lazy('personal-settings')

    def get_object(self):
        return get_personal_settings(self.request.user)