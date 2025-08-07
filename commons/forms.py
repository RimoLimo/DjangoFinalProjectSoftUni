from django import forms

from commons.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['game', 'title', 'content', 'rating']