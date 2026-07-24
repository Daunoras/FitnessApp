from django.shortcuts import render

from personal_goals.services import get_user_current_goals


def homepage(request):
    context = {}
    if request.user.is_authenticated:
        goals = get_user_current_goals(request.user)
        context = {'goals': goals}
    return render(request, 'homepage.html', context=context)
