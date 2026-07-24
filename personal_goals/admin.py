from django.contrib import admin

from .models import BodyweightGoal, DailyNutritionGoal, LiftingGoal


admin.site.register(BodyweightGoal)
admin.site.register(DailyNutritionGoal)
admin.site.register(LiftingGoal)

