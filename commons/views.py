from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView

from commons.forms import ReviewForm
from commons.models import Review
from games.models import Game


# from common.utils import get_organizer


# Create your views here.
class HomePage(TemplateView):
    template_name = 'home.html'

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

class SelectGameForReviewView(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'select_game_for_review.html'
    context_object_name = 'games'

class ReviewDetailView(DetailView):
    model = Review
    template_name = 'review_detail.html'
    context_object_name = 'review'

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'

    def get_initial(self):
        initial = super().get_initial()
        game_id = self.request.GET.get('game')
        if game_id:
            initial['game'] = game_id
        return initial

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('review-detail', kwargs={'pk': self.object.pk})

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'review_form.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('review-detail', kwargs={'pk': self.object.pk})

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = 'review_delete.html'

    def test_func(self):
        review = self.get_object()
        return self.request.user == review.user or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy('game-list')