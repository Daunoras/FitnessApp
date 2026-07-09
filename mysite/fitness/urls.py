from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('workouts/', views.WorkoutListView.as_view(), name='workouts'),
    path('workouts/add/', views.WorkoutCreateView.as_view(), name='workout-add'),
    path('workouts/<int:pk>', views.WorkoutDetailView.as_view(), name='workout-details'),
    path('workouts/<int:pk>/update', views.WorkoutUpdateView.as_view(), name='workout-update'),
    path('workouts/<int:pk>/delete', views.WorkoutDeleteView.as_view(), name='workout-delete'),
    path('set/<int:pk>/delete/', views.SetDeleteView.as_view(), name='set-delete'),
    path('set/<int:pk>/duplicate/', views.duplicate_set, name='set-duplicate'),
]
