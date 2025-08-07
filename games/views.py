from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from commons.models import Review
from .models import Game, Genre
from .forms import GameForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class GameListView(ListView):
    model = Game
    template_name = 'game_list.html'
    context_object_name = 'games'

class GameDetailView(DetailView):
    model = Game
    template_name = 'game_detail.html'
    context_object_name = 'game'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reviews'] = Review.objects.filter(game=self.object).order_by('-created_at')
        return context

class GameCreateView(LoginRequiredMixin, CreateView):
    model = Game
    form_class = GameForm
    template_name = 'game_form.html'
    success_url = reverse_lazy('game-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class GameUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Game
    form_class = GameForm
    template_name = 'game_form.html'
    success_url = reverse_lazy('game-list')

    def test_func(self):
        return self.request.user.is_authenticated

class GameDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Game
    template_name = 'game_delete.html'
    success_url = reverse_lazy('game-list')

    def test_func(self):
        return self.request.user.is_superuser



class GenreListView(ListView):
    model = Genre
    template_name = "genre_list.html"
    context_object_name = "genres"

class GenreAddView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def post(self, request):
        name = request.POST.get("name")
        if name:
            Genre.objects.get_or_create(name=name)
        return redirect("genre-list")

class GenreDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, pk):
        Genre.objects.filter(pk=pk).delete()
        return redirect("genre-list")

class GenreDetailView(DetailView):
    model = Genre
    template_name = 'genre_detail.html'
    context_object_name = 'genre'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['games'] = self.object.games.all()
        return context