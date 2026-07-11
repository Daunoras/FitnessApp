from django.urls import path
from . import views


urlpatterns = [
    path('chart/', views.chart_view, name='chart-view'),
    path('api/chart/data/', views.get_chart_data, name='chart-data'),
    path('api/dashboard/calendar/', views.get_calendar_data, name='calendar-data'),
]