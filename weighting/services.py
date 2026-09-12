from .models import Weighting


def calculate_bodyweight(user, date):
    records = Weighting.objects.filter(athlete=user)
    exact = records.filter(date=date).first()
    if exact:
        return exact.weight

    previous_record = records.filter(date__lt=date).order_by("-date").first()
    later_record = records.filter(date__gt=date).order_by("date").first()

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
