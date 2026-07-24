from .models import PersonalSettings


def get_personal_settings(user):
    settings, _ = PersonalSettings.objects.get_or_create(user=user)
    return settings
