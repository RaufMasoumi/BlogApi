from django.contrib import admin
from .models import Post
# Register your models here.


@admin.display(description='Title')
def formatted_title(obj):
    small_title = obj.title[:20]
    etc_title = small_title + ' ...'
    return etc_title


class PostAdmin(admin.ModelAdmin):
    list_display = [formatted_title, 'author', 'updated_at', 'status']


admin.site.register(Post, PostAdmin)
