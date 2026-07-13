from .models import Goal, GoalStatus

def get_user_current_goals(user):
    current_goals = Goal.objects.filter(user=user, status=GoalStatus.ACTIVE)
    return current_goals