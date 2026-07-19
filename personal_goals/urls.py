from django.urls import path
from . import views


urlpatterns = [
     path('', views.personal_goals_view, name='personal-goals'),
     path('add', views.BodyweightGoalCreateView.as_view(), name='bodyweight-goal-add'),
     path('<int:pk>', views.BodyweightGoalDetailView.as_view(), name='bodyweight-goal-details'),
     path('<int:pk>/update', views.BodyweightGoalUpdateView.as_view(), name='bodyweight-goal-update'),
     path('<int:pk>/delete', views.BodyweightGoalDeleteView.as_view(), name='bodyweight-goal-delete'),

]