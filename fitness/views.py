from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormMixin

from .forms import ExerciseCreateForm, SetCreateForm, WorkoutCreateForm
from .models import Exercise, Set, Workout


class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts.html'

    def get_queryset(self):
        return Workout.objects.filter(athlete=self.request.user).order_by('-date')


class WorkoutDetailView(LoginRequiredMixin, DetailView, FormMixin):
    model = Workout
    template_name = 'workout_details.html'
    form_class = SetCreateForm

    def get_success_url(self):
        return reverse_lazy('workout-details', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super(WorkoutDetailView, self).get_context_data(**kwargs)
        previous_data = self.request.session.get('last_set_data', {})

        if 'exercise_id' in previous_data:
            try:
                previous_data['exercise'] = Exercise.objects.get(id=previous_data['exercise_id'])
            except Exercise.DoesNotExist:
                previous_data['exercise'] = None
            del previous_data['exercise_id']

        previous_data['workout'] = self.object
        context['form'] = SetCreateForm(initial=previous_data)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.workout_id = self.kwargs['pk']
        form.save()

        self.request.session['last_set_data'] = {
            'exercise_id': form.cleaned_data['exercise'].id,
            'weight': form.cleaned_data['weight'],
            'reps': form.cleaned_data['reps']
        }

        return super().form_valid(form)


class WorkoutCreateView(LoginRequiredMixin, CreateView):
    model = Workout
    template_name = 'add_record.html'
    form_class = WorkoutCreateForm

    def get_success_url(self):
        return reverse_lazy('workout-details', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

    def get_initial(self):
        initial = super().get_initial()
        date = self.request.GET.get("date")
        if date:
            initial["date"] = date
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add workout information"
        context["cancel_url"] = reverse_lazy('workouts')
        return context


class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    fields = ['date', 'duration', 'type']
    template_name = 'add_record.html'

    def get_success_url(self):
        return reverse_lazy('workout-details', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

    def test_func(self):
        workout = self.get_object()
        return self.request.user == workout.athlete

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        context["page_title"] = f"{self.object}"
        context["delete_url"] = reverse_lazy('workout-delete', args=[self.object.pk])
        context["cancel_url"] = reverse_lazy('workout-details', args=[self.object.pk])
        return context


class WorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    success_url = reverse_lazy('workouts')
    template_name = 'delete.html'

    def test_func(self):
        workout = self.get_object()
        return self.request.user == workout.athlete

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_title = f"Do you really want to delete {self.object}?"
        context["page_title"] = page_title
        context["cancel_url"] = reverse_lazy('workout-details', args=[self.object.pk])
        return context


class SetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Set

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        workout_id = self.object.workout.id
        self.object.delete()
        return redirect(reverse('workout-details', kwargs={'pk': workout_id}))

    def test_func(self):
        workout = self.get_object().workout
        return self.request.user == workout.athlete


@login_required
def duplicate_set(request, pk):
    original_set = get_object_or_404(Set, id=pk)
    new_set = Set.objects.create(
        exercise=original_set.exercise,
        workout=original_set.workout,
        weight=original_set.weight,
        reps=original_set.reps,
    )
    return redirect('workout-details', pk=original_set.workout.pk)


class ExerciseCreateView(LoginRequiredMixin, CreateView):
    model = Exercise
    template_name = 'add_record.html'
    form_class = ExerciseCreateForm

    def get_success_url(self):
        return reverse_lazy('exercises')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Add a custom exercise"
        context["cancel_url"] = reverse_lazy('exercises')
        return context


class ExerciseListView(LoginRequiredMixin, ListView):
    model = Exercise
    template_name = 'exercises.html'

    def get_queryset(self):
        return Exercise.objects.filter(created_by=self.request.user)


class ExerciseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Exercise
    fields = ['name',
              'description',
              'target_muscle',
              'equipment',
              'uses_bodyweight']
    template_name = 'add_record.html'

    def get_success_url(self):
        return reverse_lazy('exercises')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

    def test_func(self):
        exercise = self.get_object()
        return self.request.user == exercise.created_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'update'
        context["page_title"] = f"{self.object.name}"
        context["delete_url"] = reverse_lazy('exercise-delete', args=[self.object.pk])
        context["cancel_url"] = reverse_lazy('exercises')
        return context


class ExerciseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Exercise
    success_url = reverse_lazy('exercises')
    template_name = 'delete.html'

    def test_func(self):
        exercise = self.get_object()
        return self.request.user == exercise.created_by

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Do you really want to delete {self.object.name}?"
        context["cancel_url"] = reverse_lazy('exercise-update', args=[self.object.pk])
        return context
