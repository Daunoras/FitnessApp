from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView


urlpatterns = [
    path('fitness/', include('fitness.urls')),
    path('nutrition/', include('nutrition.urls')),
    path('weighting/', include('weighting.urls')),
    path('data_charts/', include('data_charts.urls')),
    path('users/', include('users.urls')),
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='fitness/', permanent=True)),
    path('accounts/', include('allauth.urls')),
    path('settings/', include('personal_settings.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
