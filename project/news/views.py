from django.shortcuts import render, get_object_or_404
from datetime import datetime
from django.views.generic import ListView, DetailView,  UpdateView, CreateView, DeleteView
from .models import Post
from .filters import PostFilter
from .forms import PostForm


class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3


# class PostDetail(DetailView):
#     model = Post
#     template_name = 'post.html'
#     context_object_name = 'post'
#
#     def index(request):
#         return render(request, 'post.html') #

def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'flatpages/post.html', {'post': post})


class PostSearch(PostsList):
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filter_class = PostFilter

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(CreateView):
    template_name = 'flatpages/add.html'
    form_class = PostForm
    model = Post

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class PostUpdate(UpdateView):
    template_name = 'flatpages/edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    success_url = '/posts/'