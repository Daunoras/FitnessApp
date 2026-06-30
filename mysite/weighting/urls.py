from django.urls import path
from . import views


urlpatterns = [
    path('weighting/', views.WeightingListView.as_view(), name= 'weighting'),
    path('weighting/add', views.WeightingCreateView.as_view(), name= 'weighting-add'),
    path('weighting/<int:pk>/update', views.WeightingUpdateView.as_view(), name= 'weighting-update'),
    path('weighting/<int:pk>/delete', views.WeightingDeleteView.as_view(), name= 'weighting-delete'),
]