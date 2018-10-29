from django.db import models

# === models for Post app ===


class Post(models.Model):
    """
    The Post class defines the post (news) details. Each post has fields:

        1. title
        2. content
        3. image - photo connected with the post content
        4. created_at - date of creation
        5. updated_at - date of the last update
    """
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
