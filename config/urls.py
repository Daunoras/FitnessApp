from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('data_charts/', include('data_charts.urls')),
    path('fitness/', include('fitness.urls')),
    path('goals/', include('personal_goals.urls')),
    path('nutrition/', include('nutrition.urls')),
    path('settings/', include('personal_settings.urls')),
    path('users/', include('users.urls')),
    path('weighting/', include('weighting.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
