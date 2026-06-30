from .models import Weighting
from .forms import WeightingCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


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