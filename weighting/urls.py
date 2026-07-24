from django.urls import path

from . import views


urlpatterns = [
    path('', views.WeightingListView.as_view(), name='weighting'),
    path('add', views.WeightingCreateView.as_view(), name='weighting-add'),
    path('<int:pk>/update', views.WeightingUpdateView.as_view(), name='weighting-update'),
    path('<int:pk>/delete', views.WeightingDeleteView.as_view(), name='weighting-delete'),
]
