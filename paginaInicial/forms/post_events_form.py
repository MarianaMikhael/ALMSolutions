from django import forms
from paginaInicial.models.post_events import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'uidd',
            'summary',
            'start',
            'end',
            'location',
            'event_type',
            'service_option',
            'status',
            'description',
            'email',
            'valor',
            ]
