from .models import DayOfEating
from .forms import DayOfEatingCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy


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
