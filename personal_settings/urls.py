from django.urls import path

from . import views


urlpatterns = [
    path('', views.PersonalSettingsView.as_view(), name='personal-settings'),
]
