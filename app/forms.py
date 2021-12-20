from django.forms import ModelForm
from .models import Paper

class PaperForm(ModelForm):
    class Meta:
        model = Paper
        fields = ['title', 'comment', 'paper', 'category']