from django.contrib.auth import get_user_model
from django_filters import rest_framework as filters
from posts.models import Comment, Reply
from posts.filters import PostFilterSet


class CustomUserFilterSet(filters.FilterSet):

    class Meta:
        model = get_user_model()
        exact_icontains_list = ['exact', 'icontains']
        fields = {
            'username': exact_icontains_list,
            'first_name': exact_icontains_list,
            'last_name': exact_icontains_list,
            'is_staff': ['exact', ],
            'is_superuser': ['exact', ],
        }


# No need to test
class UserPostFilterSet(PostFilterSet):
    author = None


class UserCommentFilterSet(filters.FilterSet):
    post_icontains = filters.CharFilter(field_name='post__title', lookup_expr='icontains',
                                        label='Post contains')

    class Meta:
        model = Comment
        fields = ['post_icontains', ]


class UserReplyFilterSet(filters.FilterSet):
    comment_icontains = filters.CharFilter(field_name='comment__comment', lookup_expr='icontains',
                                           label='Comment contains')

    class Meta:
        model = Reply
        fields = ['comment_icontains', ]
