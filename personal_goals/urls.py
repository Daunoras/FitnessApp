from django.urls import path

from . import views


urlpatterns = [
     path('', views.personal_goals_view, name='personal-goals'),
     path('bodyweight/add', views.BodyweightGoalCreateView.as_view(), name='bodyweight-goal-add'),
     path('bodyweight/<int:pk>', views.BodyweightGoalDetailView.as_view(), name='bodyweight-goal-details'),
     path('bodyweight/<int:pk>/update', views.BodyweightGoalUpdateView.as_view(), name='bodyweight-goal-update'),
     path('bodyweight/<int:pk>/delete', views.BodyweightGoalDeleteView.as_view(), name='bodyweight-goal-delete'),
     path('bodyweight/<int:pk>/activate', views.activate_bodyweight_goal, name='bodyweight-goal-activate'),
     path('nutrition/add', views.DailyNutritionGoalCreateView.as_view(), name='nutrition-goal-add'),
     path('nutrition/<int:pk>', views.DailyNutritionGoalDetailView.as_view(), name='nutrition-goal-details'),
     path('nutrition/<int:pk>/update', views.DailyNutritionGoalUpdateView.as_view(), name='nutrition-goal-update'),
     path('nutrition/<int:pk>/delete', views.DailyNutritionGoalDeleteView.as_view(), name='nutrition-goal-delete'),
     path('lifting/add', views.LiftingGoalCreateView.as_view(), name='lifting-goal-add'),
     path('lifting/<int:pk>', views.LiftingGoalDetailView.as_view(), name='lifting-goal-details'),
     path('lifting/<int:pk>/update', views.LiftingGoalUpdateView.as_view(), name='lifting-goal-update'),
     path('lifting/<int:pk>/delete', views.LiftingGoalDeleteView.as_view(), name='lifting-goal-delete'),
]