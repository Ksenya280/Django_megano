from django import forms
from .models import Profile


class Balance(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('balance',)
