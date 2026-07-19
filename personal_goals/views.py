from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from .services import get_user_current_goals, get_user_goals
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BodyweightGoal
from .forms import BodyweightGoalCreateForm
from django.urls import reverse_lazy


def personal_goals_view(request):
    current_goals = get_user_current_goals(request.user)
    all_goals = get_user_goals(request.user)
    context = {
        "current_goals": current_goals,
        "all_goals": all_goals
    }
    return render(request, 'personal_goals.html', context)


class BodyweightGoalCreateView(LoginRequiredMixin, CreateView):
    model = BodyweightGoal
    template_name = 'bodyweight_goal_add.html'
    form_class = BodyweightGoalCreateForm

    def get_success_url(self):
        return reverse_lazy('bodyweight-goal-details', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BodyweightGoalDetailView(LoginRequiredMixin, DetailView):
    model = BodyweightGoal
    template_name = 'bodyweight_goal_details.html'


class BodyweightGoalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = BodyweightGoal
    fields = [
        'start_date',
        'deadline',
        'status',
        'target_bodyweight',
        'start_bodyweight'
    ]
    template_name = 'bodyweight_goal_add.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('bodyweight-goal-details', args=[pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        goal = self.get_object()
        return self.request.user == goal.user


class BodyweightGoalDeleteView(LoginRequiredMixin, DeleteView):
    model = BodyweightGoal
    success_url = reverse_lazy('personal-goals')
    template_name = 'bodyweight_goal_delete.html'

    def test_func(self):
        goal = self.get_object()
        return self.request.user == goal.user
