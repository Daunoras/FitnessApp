from django.urls import path
from . import views


urlpatterns = [
     path('', views.personal_goals_view, name='personal-goals'),

]