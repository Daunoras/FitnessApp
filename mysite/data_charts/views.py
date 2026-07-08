from django.shortcuts import render
from django.http import JsonResponse
from fitness.models import Exercise, Set, Workout
from nutrition.models import DayOfEating
from weighting.models import Weighting
from datetime import date, timedelta


def chart_view(request):
    lifts = Exercise.objects.all()

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
                max = (int(set.weight) * (1 + set.reps / 30)) if int(set.weight) > 0 else (1 + set.reps / 30)
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

    current_day = start
    workout_type = ''
    while current_day <= end:
        is_today = False
        is_future = False
        if current_day == today:
            is_today = True
        elif current_day > today:
            is_future = True

        for workout in workouts:
            if workout.date == current_day:
                workout_type = workout.type.name

        day_info = {'date': current_day, 'is_today': is_today, 'is_future': is_future, 'workout_type': workout_type}
        days.append(day_info)
        workout_type = ''
        current_day += timedelta(days=1)

    return JsonResponse(days, safe=False)