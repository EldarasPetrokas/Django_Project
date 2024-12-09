from django import forms
from .models import UzsakymoKomentaras, Profilis
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):
    class Meta:
        model = UzsakymoKomentaras
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Palikite komentarą...'}),
        }


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfilisUpdateForm(forms.ModelForm):
    class Meta:
        model = Profilis
        fields = ['nuotrauka']
