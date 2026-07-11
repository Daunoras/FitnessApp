from django.urls import path
from . import views


urlpatterns = [
    path('', views.personal_settings_view, name= 'personal-settings'),

]