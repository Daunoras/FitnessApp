from django.contrib import admin
from .models import DayOfEating

class DayOfEatingAdmin(admin.ModelAdmin):
    list_display = ('date', 'kcal', 'protein', 'athlete')

admin.site.register(DayOfEating)
