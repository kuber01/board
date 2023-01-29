from django.shortcuts import redirect
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Post, Response
from .forms import PostForm, ResponseForm
from .filters import PostFilter


def accept_response(request, pk):
    called_response = Response.objects.get(id=pk)
    called_response.status = True
    called_response.save()
    return redirect('response_list')


def delete_response(request, pk):
    called_response = Response.objects.get(id=pk)
    called_response.delete()
    return redirect('response_list')


class PostList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-date']
    paginate_by = 10


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'post_add.html'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    template_name = 'post_add.html'
    permission_required = ('posts.add_post', 'posts.change_post')
    form_class = PostForm
    success_url = '/'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostRespond(LoginRequiredMixin, CreateView):
    model = Response
    template_name = 'post_response.html'
    form_class = ResponseForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = Post.objects.get(id=self.kwargs.get('pk'))
        return super().form_valid(form)


class ResponseList(LoginRequiredMixin, ListView):
    model = Response
    context_object_name = 'responses'
    template_name = 'responses.html'
    ordering = ['-date']

    def get_queryset(self, **kwargs):
        queryset = Response.objects.filter(post__author=self.request.user)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context
