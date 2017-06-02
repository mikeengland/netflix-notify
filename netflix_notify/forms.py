from django import forms
from .models import Watcher


class WatcherForm(forms.ModelForm):
    """
    Form for validating the Watcher form input
    """
    title = forms.CharField(max_length=128)
    email = forms.EmailField()

    class Meta:
        model = Watcher
        fields = ('title', 'email')
