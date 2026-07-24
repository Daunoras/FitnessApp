from django.contrib import admin

from .models import Muscle, Equipment, Exercise, Workout, WorkoutType, Set


admin.site.register(Muscle)
admin.site.register(Equipment)
admin.site.register(Exercise)
admin.site.register(WorkoutType)
admin.site.register(Workout)
admin.site.register(Set)
