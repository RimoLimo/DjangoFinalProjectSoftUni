from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Game, Genre

class GameViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.superuser = User.objects.create_superuser(username='admin', password='12345')
        self.genre = Genre.objects.create(name='Action')
        self.game = Game.objects.create(
            title='Test Game',
            description='Test Description',
            genre=self.genre,
            cover_image_url='https://upload.wikimedia.org/wikipedia/commons/8/85/Smiley.svg'
        )

    def test_game_create_post(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('game-form')
        data = {
            'title': 'New Game',
            'description': 'Desc',
            'genre': self.genre.id,
            'cover_image_url': 'https://upload.wikimedia.org/wikipedia/commons/8/85/Smiley.svg',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

    def test_game_delete_post_not_superuser(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('game-delete', kwargs={'pk': self.game.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)

    def test_game_delete_post_superuser(self):
        self.client.login(username='admin', password='12345')
        url = reverse('game-delete', kwargs={'pk': self.game.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)

    def test_game_delete_view_permission(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('game-delete', kwargs={'pk': self.game.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        self.client.logout()
        self.client.login(username='admin', password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
