from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.template import loader
from bialjam.core import CustomHttpResponse
from post.models import Post
from django.utils.translation import ugettext_lazy as _

# === Views for Post app ===

"""
 Post app includes the following views:

 1. **Post detail** - Show detail chosen post  (jump to section in [[views.py#post_detail]] )
 2. **List of all posts** - Return list of all posts.  (jump to section in [[views.py#post_list]] )
 """


# === post_detail ===
def post_detail(request, id):
    """
    Show detail chosen post
    """
    template = loader.get_template('post/post_detail.html')
    try:
        post = Post.objects.get(pk=id)
    except Post.DoesNotExist:
        messages.error(request, _('Post does not exist'))
        return CustomHttpResponse.send(template, {}, request)

    context = {'post': post}
    return CustomHttpResponse.send(template, context, request)


# === post list ===
def post_list(request):
    """
    Return list of all posts.
    """
    template = loader.get_template('post/post_list.html')

    posts = Post.objects.all().order_by('created_at')
    if posts is None:
        messages.error(request, _('No posts'))
        return CustomHttpResponse.send(template, {}, request)
    context = {'posts': posts}

    return CustomHttpResponse.send(template, context, request)
