from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import DayOfEating, Weighting, Workout
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import DayOfEatingCreateForm, UserUpdateForm, ProfileUpdateForm, WeightingCreateForm, WorkoutCreateForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required

def index(request):
    context = {}
    return render(request, 'index.html', context=context)

class DaysOfEatingListView(LoginRequiredMixin, ListView):
    model = DayOfEating
    template_name = 'days_of_eating.html'

    def get_queryset(self):
        return DayOfEating.objects.filter(athlete=self.request.user).order_by('-date')


class DayOfEatingDetailView(LoginRequiredMixin, DetailView):
    model = DayOfEating
    template_name = 'day_of_eating_details.html'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'action' in request.POST:
            action = request.POST['action']
            if action == 'Add calories':
                number = request.POST.get('calories')
                self.object.add_calories(int(number))
            elif action == 'Add protein':
                number = request.POST.get('protein')
                self.object.add_protein(int(number))
            self.object.save()

        return self.get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('nutrition-details', kwargs={'pk': self.object.pk})

class DayOfEatingCreateView(LoginRequiredMixin, CreateView):
    model = DayOfEating
    success_url = reverse_lazy('nutrition')
    template_name = 'nutrition_add.html'
    form_class = DayOfEatingCreateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

class DayOfEatingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DayOfEating
    fields = ['kcal', 'protein']
    template_name = 'nutrition_add.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('nutrition-details', args=[pk])

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

    def test_func(self):
        day = self.get_object()
        return self.request.user == day.athlete

class DayOfEatingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = DayOfEating
    success_url = reverse_lazy('nutrition')
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

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profile updated")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }

    return render(request, 'profile.html', context)

class WeightingListView(LoginRequiredMixin, ListView):
    model = Weighting
    template_name = 'weighting.html'
    def get_queryset(self):
        return Weighting.objects.filter(athlete=self.request.user).order_by('-date')

class WeightingCreateView(LoginRequiredMixin, CreateView):
    model = Weighting
    success_url = reverse_lazy('weighting')
    template_name = 'weighting_add.html'
    form_class = WeightingCreateForm

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'create'
        return context

class WeightingUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Weighting
    fields = ['weight', 'date']
    template_name = 'weighting_add.html'
    success_url = reverse_lazy('weighting')

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

    def test_func(self):
        day = self.get_object()
        return self.request.user == day.athlete

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        return context

class WeightingDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Weighting
    success_url = reverse_lazy('weighting')
    template_name = 'weighting_delete.html'

    def test_func(self):
        day = self.get_object()
        return self.request.user == day.athlete

class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts.html'
    def get_queryset(self):
        return Workout.objects.filter(athlete=self.request.user).order_by('-date')

class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = 'workout_details.html'

class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    success_url = reverse_lazy('workouts')
    template_name = 'workout_add.html'
    form_class = WorkoutCreateForm

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)