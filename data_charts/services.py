from fitness.models import Set
from fitness.services import calculate_lift_max
from nutrition.models import DayOfEating
from weighting.models import Weighting


def get_nutrition_chart_data(user, date_from, date_to):
    nutrition_data = DayOfEating.objects.filter(athlete=user)
    if date_from:
        nutrition_data = nutrition_data.filter(date__gte=date_from)
    if date_to:
        nutrition_data = nutrition_data.filter(date__lte=date_to)
    labels = [day.date for day in nutrition_data]
    data = [day.kcal for day in nutrition_data]
    return labels, data


def get_weighting_chart_data(user, date_from, date_to):
    weighting_data = Weighting.objects.filter(athlete=user)
    if date_from:
        weighting_data = weighting_data.filter(date__gte=date_from)
    if date_to:
        weighting_data = weighting_data.filter(date__lte=date_to)
    labels = [weighting.date for weighting in weighting_data]
    data = [weighting.weight for weighting in weighting_data]
    return labels, data


def get_exercise_chart_data(user, lift, date_from, date_to):
    exercise_data = Set.objects.filter(workout__athlete=user, exercise=lift)
    if date_from:
        exercise_data = exercise_data.filter(workout__date__gte=date_from)
    if date_to:
        exercise_data = exercise_data.filter(workout__date__lte=date_to)
    maxes = {}
    for set_ in exercise_data:
        date = set_.workout.date
        max_ = calculate_lift_max(set_.weight, set_.reps, set_.exercise, date)
        if (date in maxes and max_ > maxes[date]) or date not in maxes:
            maxes[date] = max_
    labels = []
    data = []
    for key in maxes:
        labels.append(key)
        data.append(maxes[key])
    return labels, data
