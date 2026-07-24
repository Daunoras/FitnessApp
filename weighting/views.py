from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import WeightingCreateForm
from .models import Weighting


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

    def get_initial(self):
        initial = super().get_initial()

        date = self.request.GET.get("date")
        if date:
            initial["date"] = date

        return initial


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
    template_name = 'delete.html'

    def test_func(self):
        day = self.get_object()
        return self.request.user == day.athlete

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Do you really want to delete {self.object.date}?"
        context["cancel_url"] = reverse_lazy('weighting')
        return context
