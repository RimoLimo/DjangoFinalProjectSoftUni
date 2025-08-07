from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from commons.models import Review, Game

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.game = Game.objects.create(title='Test Game')
        self.review = Review.objects.create(
            user=self.user,
            game=self.game,
            title='Great Game',
            content='Really enjoyed it',
            rating=8
        )

    def test_review_str(self):
        self.assertEqual(str(self.review), f"Review by {self.user.username} for {self.game.title}")

    def test_review_rating_limits(self):
        self.assertTrue(0 <= self.review.rating <= 10)


class ReviewViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.game = Game.objects.create(title='Test Game')
        self.review = Review.objects.create(
            user=self.user,
            game=self.game,
            title='Great Game',
            content='Really enjoyed it',
            rating=8
        )

    def test_review_detail_view(self):
        url = reverse('review-detail', kwargs={'pk': self.review.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Great Game')

    def test_review_create_view_requires_login(self):
        url = reverse('review-add')
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login

        self.client.login(username='testuser', password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_review_create_post(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('review-add')
        data = {
            'title': 'New Review',
            'content': 'Awesome game!',
            'rating': 9,
            'game': self.game.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(Review.objects.filter(title='New Review').exists())

    def test_review_update_view_permission(self):
        url = reverse('review-edit', kwargs={'pk': self.review.pk})

        # Not logged in user redirected
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='testuser', password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_review_delete_view_permission(self):
        url = reverse('review-delete', kwargs={'pk': self.review.pk})

        # Not logged in user redirected
        response = self.client.get(url)
        self.assertNotEqual(response.status_code, 200)

        self.client.login(username='testuser', password='12345')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_review_delete_post(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('review-delete', kwargs={'pk': self.review.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())
