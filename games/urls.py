from django.urls import path

from games import views
from games.views import GameListView, GameDetailView, GameCreateView, GameUpdateView, GameDeleteView, GenreListView

urlpatterns = [
    path('', GameListView.as_view(), name='game-list'),
    path('<int:pk>/', GameDetailView.as_view(), name='game-detail'),
    path('create/', GameCreateView.as_view(), name='game-form'),
    path('<int:pk>/edit/', GameUpdateView.as_view(), name='game-edit'),
    path('<int:pk>/delete/', GameDeleteView.as_view(), name='game-delete'),
    path('genres/', GenreListView.as_view(), name='genre-list'),
]