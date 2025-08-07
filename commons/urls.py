from django.urls import path

from commons.views import HomePage, ReviewCreateView, ReviewDetailView, ReviewUpdateView, ReviewDeleteView, \
    SelectGameForReviewView

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('reviews/add/', ReviewCreateView.as_view(), name='review-add'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('reviews/<int:pk>/edit/', ReviewUpdateView.as_view(), name='review-edit'),
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),
    path('reviews/select-game/', SelectGameForReviewView.as_view(), name='select-game-for-review'),
]