from django.shortcuts import render
from django.http import JsonResponse
from fitness.models import Exercise, Set, Workout
from nutrition.models import DayOfEating
from weighting.models import Weighting
from datetime import date, timedelta
from personal_settings.services import get_personal_settings
from personal_settings.models import ExerciseChoices
from django.db.models import Q
from django.conf import settings

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


def calculate_bodyweight(date):
    exact = Weighting.objects.filter(date=date).first()
    if exact:
        return exact.weight

    previous_record = Weighting.objects.filter(date__lt=date).order_by("-date").first()
    later_record = Weighting.objects.filter(date__gt=date).order_by("date").first()

    if previous_record and later_record:
        total_days = (later_record.date - previous_record.date).days
        elapsed_days = (date - previous_record.date).days
        coefficient = elapsed_days / total_days
        return previous_record.weight + coefficient * (later_record.weight - previous_record.weight)
    elif previous_record:
        return previous_record.weight
    elif later_record:
        return later_record.weight
    else:
        return 0


def calculate_lift_max(weight, reps, exercise, date):
    if exercise.uses_bodyweight:
        bodyweight = calculate_bodyweight(date)
        total_weight = int(weight) + bodyweight
        estimated_max = (total_weight * (1 + reps / 30)) - bodyweight
    else:
        estimated_max = (int(weight) * (1 + reps / 30))
    return estimated_max


def get_chart_data(request):
    if request.user.is_authenticated:

        model_name = request.GET.get('model')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        lift = request.GET.get('lift')

        if model_name == 'nutrition':
            nutrition_data = DayOfEating.objects.filter(athlete=request.user)
            if date_from:
                nutrition_data = nutrition_data.filter(date__gte=date_from)
            if date_to:
                nutrition_data = nutrition_data.filter(date__lte=date_to)
            labels = [day.date for day in nutrition_data]
            data = [day.kcal for day in nutrition_data]
        elif model_name == 'weight':
            weighting_data = Weighting.objects.filter(athlete=request.user)
            if date_from:
                weighting_data = weighting_data.filter(date__gte=date_from)
            if date_to:
                weighting_data = weighting_data.filter(date__lte=date_to)
            labels = [weighting.date for weighting in weighting_data]
            data = [weighting.weight for weighting in weighting_data]
        elif model_name == 'exercise':
            exercise_data = Set.objects.filter(workout__athlete=request.user, exercise=lift)
            if date_from:
                exercise_data = exercise_data.filter(workout__date__gte=date_from)
            if date_to:
                exercise_data = exercise_data.filter(workout__date__lte=date_to)
            maxes = {}
            for set in exercise_data:
                date = set.workout.date
                max = calculate_lift_max(set.weight, set.reps, set.exercise, date)
                if (date in maxes and max > maxes[date]) or date not in maxes:
                   maxes[date] = max
            labels = []
            data = []
            for key in maxes:
                labels.append(key)
                data.append(maxes[key])
        else:
            return JsonResponse({'error': 'Invalid model'}, status=400)

    else:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({
        'labels': labels,
        'data': data,
    })


def get_calendar_data(request):
    days = []

    today = date.today()

    start = today - timedelta(days=30)
    start = start - timedelta(days=start.weekday())

    end = today
    if end.weekday() != 6:
        end = end + timedelta(days=(6 - end.weekday()))

    workouts = Workout.objects.filter(athlete=request.user, date__gte=start)
    nutrition = DayOfEating.objects.filter(athlete=request.user, date__gte=start)
    weighting = Weighting.objects.filter(athlete=request.user, date__gte=start)

    current_day = start
    workout_type = ''
    eating_info = ''
    weight_info = ''

    nutrition_add_url = ''
    nutrition_view_url = ''
    weighting_add_url = ''
    weighting_view_url = ''
    workout_add_url = ''
    workout_view_url = ''

    while current_day <= end:
        is_today = False
        is_future = False
        if current_day == today:
            is_today = True
        elif current_day > today:
            is_future = True

        workout_add_url = f"workouts/add/?date={current_day.isoformat()}"
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

        day_info = {'date': current_day,
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
                    'viewWeightingURL': weighting_view_url}
        days.append(day_info)
        workout_type = ''
        eating_info = ''
        weight_info = ''
        nutrition_add_url = ''
        nutrition_view_url = ''
        weighting_add_url = ''
        weighting_view_url = ''
        workout_add_url = ''
        workout_view_url = ''
        current_day += timedelta(days=1)

    return JsonResponse(days, safe=False)