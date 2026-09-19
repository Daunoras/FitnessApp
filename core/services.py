from django.contrib.auth.mixins import LoginRequiredMixin


class AthleteOwnedMixin(LoginRequiredMixin):
    def get_queryset(self):
        return super().get_queryset().filter(athlete=self.request.user)
