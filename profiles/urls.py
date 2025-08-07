from django.urls import path
from .views import ProfileDetailView, ProfileUpdateView, ProfileDeleteView

urlpatterns = [
    path('me/', ProfileDetailView.as_view(), name='profile-detail'),
    path('me/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('me/delete/', ProfileDeleteView.as_view(), name='profile-delete'),
]
