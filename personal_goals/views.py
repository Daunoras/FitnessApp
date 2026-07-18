from django.shortcuts import render
from .services import get_user_current_goals


def personal_goals_view(request):
    current_goals = get_user_current_goals(request.user)
    context = {
        "current_goals": current_goals
    }
    return render(request, 'personal_goals.html', context)
