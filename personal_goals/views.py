from django.shortcuts import render

def personal_goals_view(request):
    context = {}
    return render(request, 'personal_goals.html', context)
