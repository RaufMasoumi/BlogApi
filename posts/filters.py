from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from .models import Post, Comment, Reply


class PostFilterSet(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username', lookup_expr='exact', label='Author')
    topic_icontains = filters.CharFilter(field_name='tags__title', lookup_expr='icontains',
                                         label='Topic contains')

    class Meta:
        model = Post
        icontains_list = ['icontains', ]
        fields = {
            'title': icontains_list,
            'description': icontains_list,
            'status': ['exact', ]
        }

    @property
    def qs(self):
        parent = super().qs
        user = getattr(self.request, 'user', None)
        if isinstance(user, get_user_model()) and user.is_staff:
            return parent

        elif isinstance(user, get_user_model()) and not user.is_staff:
            return parent.filter(status='p') | parent.filter(author=user)

        return parent.filter(status='p')


class CommentFilterSet(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username', lookup_expr='exact', label='Author')

    class Meta:
        model = Comment
        fields = ['author', ]


class ReplyFilterSet(filters.FilterSet):
    author = filters.CharFilter(field_name='author__username', lookup_expr='exact', label='Author')

    class Meta:
        model = Reply
        fields = ['author', ]
