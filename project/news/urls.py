from django.urls import path
from .views import *
from .import views
from django.views.decorators.cache import cache_page

urlpatterns = [
   path('', cache_page(60)(PostsList.as_view()), name='posts'),
   # path('<int:pk>', PostDetail.as_view()), #
   path('post/<int:pk>', views.post, name='post'),
   # path('post/<int:pk>', cache_page(300)(views.post), name='post'),
   path('search/', PostSearch.as_view(), name='search'),
   path('add/', PostCreate.as_view(), name='add'),
   path('edit/<int:pk>', PostUpdate.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDelete.as_view(), name='post_delete'),
   path('user/', UserUpdateView.as_view(), name='user_update'),
   path('category/', CategorySubscribeView.as_view()),
   path('category/<int:pk>', subscribe_category, name='subscribe_category'),
]

