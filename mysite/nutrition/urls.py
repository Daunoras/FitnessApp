from django.urls import path
from . import views


urlpatterns = [
    path('', views.DaysOfEatingListView.as_view(), name='nutrition'),
    path('<int:pk>', views.DayOfEatingDetailView.as_view(), name='nutrition-details'),
    path('add', views.DayOfEatingCreateView.as_view(), name='nutrition-add'),
    path('<int:pk>/update', views.DayOfEatingUpdateView.as_view(), name='nutrition-update'),
    path('<int:pk>/delete', views.DayOfEatingDeleteView.as_view(), name='nutrition-delete'),
]