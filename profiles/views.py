
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from profiles.forms import ProfileForm
from profiles.models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile_detail.html'

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('profile-detail')

    def get_object(self):

        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return self.request.user.profile

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = Profile
    template_name = 'profile_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)

    def post(self, request, *args, **kwargs):
        user = request.user
        user.delete()
        return HttpResponseRedirect(self.success_url)



print("ProfileDeleteView loaded")