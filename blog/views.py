from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, Country, Place


def home(request):
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }

    return render(request, 'blog/home.html', context) # get context and request to home.html


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html' # default: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted'] # sorted date posted from new to old
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts_list'] = Post.objects.filter(published=True).order_by('-date_posted')[:3]
        context['countries'] = Country.objects.all()
        return context
    
    def get_queryset(self):
        country = get_object_or_404(Country, id=self.kwargs.get('id'))
        return Post.objects.filter(country=country).order_by('-date_posted')

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # default: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(FormMixin, DetailView):
    form_class = CommentForm
    model = Post

    def get_success_url(self):
        return reverse('post-detail', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['form'] = CommentForm
        context['comments'] = self.object.comments.filter(approved=True)
        return context

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':  
            comm_form = CommentForm(request.POST)
            comm_form.instance.post = Post.objects.get(id=self.kwargs.get('pk'))
            comm_form.instance.user = self.request.user 
            comm_form.save()
            return redirect('post-detail', pk=self.kwargs.get('pk'))
        else:
            return redirect('post-detail', pk=self.kwargs.get('pk'))
    


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'country', 'place', 'image']
    success_message = 'Tạo bài viết thành công!'

    
    def form_valid(self, form):
        post = form.save(commit=False)
        image = form.cleaned_data['image']
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    

class PostUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/update.html'
    fields = ['title', 'content', 'place', 'image']
    success_message = 'Bài viết đã được cập nhật!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, DeleteView):
    model = Post
    success_message = 'Xóa bài viết thành công!'
    success_url = '/'
    
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, self.success_message)
        return super(PostDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def PostLikeView(request, pk):
    if request.method == 'POST':
        user = request.user
        post = get_object_or_404(Post, id=request.POST.get('post_id'))
        _liked = user in post.liked.all()
        if _liked :
            post.liked.remove(user)
        else:
            post.liked.add(user)

    return redirect('post-detail', pk=post.id)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})