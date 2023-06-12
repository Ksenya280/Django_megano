from django import forms
from django.forms import ModelForm

from .models import CommentProduct


class CommentForm(ModelForm):
    content = forms.CharField(
        max_length=500, required=True, widget=forms.Textarea(
            attrs={
                'class': 'form-textarea',
                'data-validate': 'require',
                'placeholder': 'Отзыв',
                'cols': '100',
                'rows': '2'
            }))

    class Meta:
        model = CommentProduct
        fields = 'content',
