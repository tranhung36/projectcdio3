from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.db.models import Count
from django.views.generic.edit import FormMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from .forms import CommentForm, ImagesForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    RedirectView
)
from .models import Post, Comment, Country, Place, Images


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
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['featured_post'] = Post.objects.annotate(like_count=Count('liked')).order_by('-like_count')[:3]
        return context


class SearchPostView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(title__icontains=query)
        else:
            return Post.objects.all()
            

class CountryListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(CountryListView, self).get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        context['country'] = Country.objects.filter(id=self.kwargs.get('id')).first()
        context['featured_post'] = Post.objects.annotate(like_count=Count('liked')).order_by('-like_count')[:5]
        return context

    def get_queryset(self):
        country = get_object_or_404(Country, id=self.kwargs.get('id'))
        return Post.objects.filter(country=country).order_by('-date_posted')


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html' # default: <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        return context
    
    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')



class PostDetailView(SuccessMessageMixin, FormMixin, DetailView):
    form_class = CommentForm
    model = Post
    success_message = 'Bình luận thành công!'
    
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        country = Post.objects.get(id=self.kwargs.get('pk')).country
        context['form'] = CommentForm
        context['countries'] = Country.objects.all()
        context['comments'] = self.object.comments.filter(approved=True, parent__isnull=True)
        context['post_list'] = Post.objects.filter(country_id=country).order_by('-date_posted')[:3]
        return context

    def post(self, request, *args, **kwargs):
        comm_form = self.form_class(request.POST)
        if comm_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                if parent_obj:
                    replay_comment = comm_form.save(commit=False)
                    replay_comment.parent = parent_obj
            comm_form.instance.post = Post.objects.get(id=self.kwargs.get('pk'))
            comm_form.instance.user = self.request.user
            comm_form.save()


class PostCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    ImagesFormSet = modelformset_factory(Images, form=ImagesForm, extra=3)
    success_message = 'Tạo bài viết thành công!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["postForm"] = PostForm
        context['countries'] = Country.objects.all()
        context["formset"] = self.ImagesFormSet(queryset=Images.objects.none())
        return context
    
    def post(self, request, *args, **kwargs):
        postForm = self.form_class(request.POST, request.FILES or None)
        formset = self.ImagesFormSet(request.POST, request.FILES, queryset=Images.objects.none())
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.author = self.request.user
            post_form.save()
            for form in formset.cleaned_data:
                if form:
                    images = form['images']
                    photo = Images(post=post_form, images=images)
                    photo.save()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'postForm': postForm, 'formset': formset})


class PostUpdateView(SuccessMessageMixin, UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/update.html'
    form_class = PostForm
    success_message = 'Bài viết đã được cập nhật!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        return context

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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countries'] = Country.objects.all()
        return context

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
    countries = Country.objects.all()
    context = {
        'countries': countries
    }
    return render(request, 'blog/about.html', {'title': 'About', 'countries':countries})