from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import DayOfEating
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import DayOfEatingCreateForm

def index(request):
    context = {}
    return render(request, 'index.html', context=context)

class DaysOfEatingListView(LoginRequiredMixin, ListView):
    model = DayOfEating
    template_name = 'days_of_eating.html'

    def get_queryset(self):
        return DayOfEating.objects.filter(athlete=self.request.user)


class DayOfEatingDetailView(LoginRequiredMixin, DetailView):
    model = DayOfEating
    template_name = 'day_of_eating_details.html'


class DayOfEatingCreateView(LoginRequiredMixin, CreateView):
    model = DayOfEating
    success_url = "/fitness/nutrition"
    template_name = 'nutrition_add.html'
    form_class = DayOfEatingCreateForm

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

class DayOfEatingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DayOfEating
    fields = ['kcal', 'protein']
    success_url = "/fitness/nutrition"
    template_name = 'nutrition_add.html'

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

    def test_func(self):
        day = self.get_object()
        return self.request.user == day.athlete

class DayOfEatingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DayOfEating
    success_url = "/fitness/nutrition"
    template_name = 'nutrition_delete.html'

    def test_func(self):
        day = self.get_object()
        return self.request.user == day.athlete


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Username {username} is already taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'The email adress {email} is already taken')
                    return redirect('register')
                else:
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} has been registered')
                    return redirect('login')
        else:
            messages.error(request, 'The passwords do not match')
            return redirect('register')
    return render(request, 'register.html')