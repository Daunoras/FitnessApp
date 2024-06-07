from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('nutrition/', views.DaysOfEatingListView.as_view(), name='nutrition'),
    path('register/', views.register, name='register'),
    path('nutrition/<int:pk>', views.DayOfEatingDetailView.as_view(), name='nutrition-details'),
    path('nutrition/add', views.DayOfEatingCreateView.as_view(), name='nutrition-add'),
    path('nutrition/<int:pk>/update', views.DayOfEatingUpdateView.as_view(), name='nutrition-update'),
    path('nutrition/<int:pk>/delete', views.DayOfEatingDeleteView.as_view(), name='nutrition-delete'),

]