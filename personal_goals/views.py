from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .forms import BodyweightGoalCreateForm, DailyNutritionGoalCreateForm, LiftingGoalCreateForm
from .models import BodyweightGoal, DailyNutritionGoal, LiftingGoal
from .services import get_user_current_goals, get_user_goals


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
    template_name = 'add_record.html'
    form_class = BodyweightGoalCreateForm

    def get_success_url(self):
        return reverse_lazy('bodyweight-goal-details', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add a goal for your bodyweight"
        context["cancel_url"] = reverse_lazy('personal-goals')
        return context


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
    template_name = 'add_record.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('bodyweight-goal-details', args=[pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        goal = self.get_object()
        return self.request.user == goal.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        context["page_title"] = f"{self.object}"
        context["delete_url"] = reverse_lazy('bodyweight-goal-delete', args=[self.object.pk])
        context["cancel_url"] = reverse_lazy('bodyweight-goal-details', args=[self.object.pk])
        return context


class BodyweightGoalDeleteView(LoginRequiredMixin, DeleteView):
    model = BodyweightGoal
    success_url = reverse_lazy('personal-goals')
    template_name = 'delete.html'

    def test_func(self):
        goal = self.get_object()
        return self.request.user == goal.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Do you really want to delete your bodyweight goal?"
        context["cancel_url"] = reverse_lazy('bodyweight-goal-details', args=[self.object.pk])
        return context


class DailyNutritionGoalCreateView(LoginRequiredMixin, CreateView):
    model = DailyNutritionGoal
    template_name = 'add_record.html'
    form_class = DailyNutritionGoalCreateForm

    def get_success_url(self):
        return reverse_lazy('nutrition-goal-details', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add a daily nutrition goal"
        context["cancel_url"] = reverse_lazy('personal-goals')
        return context


class DailyNutritionGoalDetailView(LoginRequiredMixin, DetailView):
    model = DailyNutritionGoal
    template_name = 'nutrition_goal_details.html'


class DailyNutritionGoalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = DailyNutritionGoal
    fields = [
        'start_date',
        'deadline',
        'status',
        'nutrient_type',
        'amount'
    ]
    template_name = 'add_record.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('nutrition-goal-details', args=[pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        goal = self.get_object()
        return self.request.user == goal.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        context["page_title"] = f"{self.object}"
        context["delete_url"] = reverse_lazy('nutrition-goal-delete', args=[self.object.pk])
        context["cancel_url"] = reverse_lazy('nutrition-goal-details', args=[self.object.pk])
        return context


class DailyNutritionGoalDeleteView(LoginRequiredMixin, DeleteView):
    model = DailyNutritionGoal
    success_url = reverse_lazy('personal-goals')
    template_name = 'delete.html'

    def test_func(self):
        goal = self.get_object()
        return self.request.user == goal.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Do you really want to delete the goal for your daily nutrition?"
        context["cancel_url"] = reverse_lazy('nutrition-goal-details', args=[self.object.pk])
        return context


class LiftingGoalCreateView(LoginRequiredMixin, CreateView):
    model = LiftingGoal
    template_name = 'add_record.html'
    form_class = LiftingGoalCreateForm

    def get_success_url(self):
        return reverse_lazy('lifting-goal-details', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add a lifting goal"
        context["cancel_url"] = reverse_lazy('personal-goals')
        return context


class LiftingGoalDetailView(LoginRequiredMixin, DetailView):
    model = LiftingGoal
    template_name = 'lifting_goal_details.html'


class LiftingGoalUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = LiftingGoal
    fields = [
            'start_date',
            'deadline',
            'status',
            'exercise',
            'weight',
            'reps',
            'is_estimated'
    ]
    template_name = 'add_record.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('lifting-goal-details', args=[pk])

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        goal = self.get_object()
        return self.request.user == goal.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        context["page_title"] = f"{self.object}"
        context["delete_url"] = reverse_lazy('lifting-goal-delete', args=[self.object.pk])
        context["cancel_url"] = reverse_lazy('lifting-goal-details', args=[self.object.pk])
        return context


class LiftingGoalDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = LiftingGoal
    success_url = reverse_lazy('personal-goals')
    template_name = 'delete.html'

    def test_func(self):
        goal = self.get_object()
        return self.request.user == goal.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Do you really want to delete your lifting goal?"
        context["cancel_url"] = reverse_lazy('lifting-goal-details', args=[self.object.pk])
        return context