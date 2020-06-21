from django import forms
from paginaInicial.models.post_events import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['summary', 'location', 'description','start','end','event_id','email']
