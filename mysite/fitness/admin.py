from django.contrib import admin
from .models import DayOfEating, Muscle, Equipment, Exercise, Workout, WorkoutType, Set

class DayOfEatingAdmin(admin.ModelAdmin):
    list_display = ('date', 'kcal', 'protein', 'athlete')



admin.site.register(DayOfEating)
admin.site.register(Muscle)
admin.site.register(Equipment)
admin.site.register(Exercise)
admin.site.register(WorkoutType)
admin.site.register(Workout)
admin.site.register(Set)
