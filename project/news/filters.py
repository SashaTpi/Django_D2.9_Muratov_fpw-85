from django_filters import FilterSet, DateTimeFromToRangeFilter, ModelChoiceFilter
from django_filters.widgets import RangeWidget
from .models import Post, Author, User



class PostFilter(FilterSet):
    dateCreation = DateTimeFromToRangeFilter(lookup_expr=(
        'icontains'), widget=RangeWidget(attrs={'type': 'datetime-local'}), label='По дате')
    author = ModelChoiceFilter(
        field_name='author__authorUser',
        queryset=User.objects.all(),
        label='По автору'
    )

    class Meta:
        model = Post

        fields = { 'title': ['icontains'],
                   # 'author': ['exact'],
                  #'postCategory': ['exact']
        }