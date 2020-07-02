from django import forms
from .models import Comment, Images, Post


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 50, 'style': 'resize:none', 'placeholder': 'Nhập gì đó...'}), label='')

    class Meta:
        model = Comment
        fields = ('content',)

class ImagesForm(forms.ModelForm):
    images = forms.ImageField(label='Hình ảnh')
    class Meta:
        model = Images
        fields = ('images',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'country', 'place', 'image',)
