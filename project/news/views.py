from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.views.generic import ListView, DetailView,  UpdateView, CreateView, DeleteView
from .models import * #Post
from .filters import PostFilter
from .forms import PostForm, AuthorForm
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required



class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    queryset = Post.objects.filter() #categoryType='NW') #
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


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
    queryset = Post.objects.filter()#categoryType='NW, AR')
    ordering = 'dateCreation'
    template_name = 'flatpages/search.html'
    context_object_name = 'search'
    filter_class = PostFilter
    paginate = 3

    def get_filter(self):
        return PostFilter(self.request.GET, queryset=super().get_queryset())

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.get_filter().qs

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['filter'] = PostFilter(
            self.request.GET, queryset=self.get_queryset())
        return context


class PostCreate(CreateView, PermissionRequiredMixin):
    # raise_exception = True ######
    template_name = 'flatpages/add.html'
    form_class = PostForm
    # model = Post
    permission_required = ('news.add_post',)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.categoryType = 'NW'
        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    template_name = 'flatpages/edit.html'
    form_class = PostForm
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(PermissionRequiredMixin, DeleteView):
    template_name = 'flatpages/delete.html'
    queryset = Post.objects.all()
    success_url = reverse_lazy('posts')
    permission_required = ('news.delete_post',)

class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'author_update.html'
    form_class = AuthorForm

    def get_object(self, **kwargs):
        return self.request.user

class CategorySubscribeView(ListView):
    model = Category
    template_name = 'flatpages/post_category.html'
    context_object_name = 'post_category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    # def get_queryset(self):
    #     self.category = get_object_or_404(Category, id=self.kwargs['pk'])
    #     queryset = Post.objects.filter(category=self.category).order_by('-date')
    #     return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
    #     context['category'] = self.category
    #     return context

@login_required
def subscribe_category(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)
    id_u = request.user.id
    email = category.subscribers.get(id=id_u).email
    send_mail(
        subject=f'News Portal: подписка на обновления категории {category}',
        message=f'«{request.user}», вы подписались на обновление категории: «{category}».',
        from_email='testpostnoname@yandex.ru',
        recipient_list=[f'{email}', ],
    )
    return redirect('/posts')

@login_required
def subscribe(request, pk):
    user = request.user
    subscriber = User.objects.filter().last()
    category = Category.objects.get(id=pk)
    category.subscribers.add(subscriber)

    html_content = render_to_string(
        'subscribe_created.html',
        {
            'subscribe': subscribe,
        }
    )

    msg = EmailMultiAlternatives(
        subject=f'Подписка на {category}',
        body=category,
        to=[user],
    )
    msg.attach_alternative(html_content, "text/html")

    msg.send()

    return redirect(request.META.get('HTTP_REFERER'))