from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        widgets = {
          'content': forms.Textarea(attrs={'rows': 3}),
        }
        fields = ('content',)
