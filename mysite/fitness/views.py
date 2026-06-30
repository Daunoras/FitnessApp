from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Workout, Set, Exercise
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import WorkoutCreateForm, SetCreateForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormMixin
from nutrition.models import DayOfEating
from weighting.models import Weighting

def index(request):
    context = {}
    return render(request, 'index.html', context=context)


class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts.html'
    def get_queryset(self):
        return Workout.objects.filter(athlete=self.request.user).order_by('-date')

class WorkoutDetailView(LoginRequiredMixin, DetailView, FormMixin):
    model = Workout
    template_name = 'workout_details.html'
    form_class = SetCreateForm
    # context_object_name = 'workout'

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
    template_name = 'workout_add.html'
    form_class = WorkoutCreateForm

    def get_success_url(self):
        return reverse_lazy('workout-details', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

class WorkoutUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Workout
    fields = ['date', 'duration', 'type']
    template_name = 'workout_add.html'

    def get_success_url(self):
        pk = self.object.pk
        return reverse_lazy('workout-details', args=[pk])

    def form_valid(self, form):
        form.instance.athlete = self.request.user
        return super().form_valid(form)

    def test_func(self):
        workout = self.get_object()
        return self.request.user == workout.athlete

class WorkoutDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Workout
    success_url = reverse_lazy('workouts')
    template_name = 'workout_delete.html'

    def test_func(self):
        workout = self.get_object()
        return self.request.user == workout.athlete

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


def chart_view(request):
    lifts = Exercise.objects.all()

    return render(
        request,
        'chart.html',
        {
            "lifts": lifts
        }
    )

def get_chart_data(request):
    if request.user.is_authenticated:

        model_name = request.GET.get('model')
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        lift = request.GET.get('lift')

        if model_name == 'nutrition':
            nutrition_data = DayOfEating.objects.filter(athlete=request.user)
            if date_from:
                nutrition_data = nutrition_data.filter(date__gte=date_from)
            if date_to:
                nutrition_data = nutrition_data.filter(date__lte=date_to)
            labels = [day.date for day in nutrition_data]
            data = [day.kcal for day in nutrition_data]
        elif model_name == 'weight':
            weighting_data = Weighting.objects.filter(athlete=request.user)
            if date_from:
                weighting_data = weighting_data.filter(date__gte=date_from)
            if date_to:
                weighting_data = weighting_data.filter(date__lte=date_to)
            labels = [weighting.date for weighting in weighting_data]
            data = [weighting.weight for weighting in weighting_data]
        elif model_name == 'exercise':
            exercise_data = Set.objects.filter(workout__athlete=request.user, exercise=lift)
            if date_from:
                exercise_data = exercise_data.filter(workout__date__gte=date_from)
            if date_to:
                exercise_data = exercise_data.filter(workout__date__lte=date_to)
            maxes = {}
            for set in exercise_data:
                date = set.workout.date
                max = (int(set.weight) * (1 + set.reps / 30)) if int(set.weight) > 0 else (1 + set.reps / 30)
                if (date in maxes and max > maxes[date]) or date not in maxes:
                   maxes[date] = max
            labels = []
            data = []
            for key in maxes:
                labels.append(key)
                data.append(maxes[key])
        else:
            return JsonResponse({'error': 'Invalid model'}, status=400)

    else:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    return JsonResponse({
        'labels': labels,
        'data': data,
    })
