from datetime import date, timedelta

from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.http import JsonResponse

from fitness.models import Exercise, Workout
from nutrition.models import DayOfEating
from personal_settings.services import get_personal_settings
from personal_settings.models import ExerciseChoices
from weighting.models import Weighting
from .services import get_nutrition_chart_data, get_weighting_chart_data, get_exercise_chart_data


def chart_view(request):
    personal_settings = get_personal_settings(request.user)
    query = Q()

    if ExerciseChoices.CUSTOM in personal_settings.exercise_pool:
        query |= Q(created_by=request.user)
    if ExerciseChoices.DEFAULT in personal_settings.exercise_pool:
        query |= Q(created_by=settings.SYSTEM_USER)
    if ExerciseChoices.EVERYONE in personal_settings.exercise_pool:
        query |= ~Q(created_by__in=[request.user, settings.SYSTEM_USER])

    lifts = Exercise.objects.filter(query)

    return render(
        request,
        'chart.html',
        {
            "lifts": lifts
        }
    )


def get_chart_data(request):
    if request.user.is_authenticated:

        model_name = request.GET.get('model')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        lift = request.GET.get('lift')

        if model_name == 'nutrition':
            data = get_nutrition_chart_data(request.user, date_from, date_to)
        elif model_name == 'weight':
            data = get_weighting_chart_data(request.user, date_from, date_to)
        elif model_name == 'exercise':
            data = get_exercise_chart_data(request.user, lift, date_from, date_to)
        else:
            return JsonResponse({'error': 'Invalid model'}, status=400)
    else:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({
        'data': data,
    })


def get_calendar_data(request):
    days = []
    today = date.today()
    start = today - timedelta(days=30)
    start = start - timedelta(days=start.weekday())
    current_day = start
    end = today
    if end.weekday() != 6:
        end = end + timedelta(days=(6 - end.weekday()))

    workouts = Workout.objects.filter(athlete=request.user, date__gte=start)
    nutrition = DayOfEating.objects.filter(athlete=request.user, date__gte=start)
    weighting = Weighting.objects.filter(athlete=request.user, date__gte=start)

    while current_day <= end:
        workout_type = ''
        eating_info = ''
        weight_info = ''
        nutrition_view_url = ''
        weighting_view_url = ''
        workout_view_url = ''

        is_today = False
        is_future = False
        if current_day == today:
            is_today = True
        elif current_day > today:
            is_future = True

        workout_add_url = f"/fitness/workouts/add/?date={current_day.isoformat()}"
        nutrition_add_url = f"/nutrition/add?date={current_day.isoformat()}"
        weighting_add_url = f"/weighting/add?date={current_day.isoformat()}"

        for day_nutrition in nutrition:
            if day_nutrition.date == current_day:
                eating_info = f"{day_nutrition.kcal}kcal, {day_nutrition.protein} g protein"
                nutrition_view_url = f"/nutrition/{day_nutrition.pk}"

        for weight in weighting:
            if weight.date == current_day:
                weight_info = f"Bodyweight: {weight.weight} kg"
                weighting_view_url = f"/weighting/{weight.pk}/update"

        for workout in workouts:
            if workout.date == current_day:
                workout_type = workout.type.name
                workout_view_url = f"workouts/{workout.pk}"

        day_info = {
            'date': current_day,
            'is_today': is_today,
            'is_future': is_future,
            'workout_type': workout_type,
            'nutritionInfo': eating_info,
            'weightInfo': weight_info,
            'addWorkoutURL': workout_add_url,
            'viewWorkoutURL': workout_view_url,
            'addNutritionURL': nutrition_add_url,
            'viewNutritionURL': nutrition_view_url,
            'addWeightingURL': weighting_add_url,
            'viewWeightingURL': weighting_view_url
        }
        days.append(day_info)
        current_day += timedelta(days=1)

    return JsonResponse(days, safe=False)
