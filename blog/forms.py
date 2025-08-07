from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets= {
            'content': forms.Textarea(attrs={
                'placeholder': 'Escreve aqui o teu comentário...',
                'class': 'form-control',
                'rows': 3})
        }