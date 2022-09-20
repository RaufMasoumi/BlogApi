from django.contrib import admin
from .models import Post, Tag, Comment, Reply, formatted_text
# Register your models here.


class CommentInline(admin.TabularInline):
    model = Comment


class ReplyInline(admin.TabularInline):
    model = Reply


@admin.display(description='Title')
def formatted_title(post):
    return formatted_text(post.title)


@admin.display(description='Comment')
def formatted_comment(comment):
    return formatted_text(comment.comment)


@admin.display(description='Reply')
def formatted_reply(reply):
    return formatted_text(reply.reply)


class PostAdmin(admin.ModelAdmin):
    list_display = [formatted_title, 'author', 'updated_at', 'status']
    inlines = [CommentInline, ]


class CommentAdmin(admin.ModelAdmin):
    list_display = [formatted_comment, 'author', 'commented_at', 'updated_at']
    inlines = [ReplyInline, ]


class ReplyAdmin(admin.ModelAdmin):
    list_display = [formatted_reply, 'author', 'replied_at', 'updated_at']
    inlines = [ReplyInline, ]


admin.site.register(Tag)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply, ReplyAdmin)
