from django import forms
from paginaInicial.models.post import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['summary', 'location', 'description','start','end','event_id','email']
