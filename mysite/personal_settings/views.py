from django.shortcuts import render


def personal_settings_view(request):
    context = {}
    return render(request, 'personal_settings.html', context=context)
