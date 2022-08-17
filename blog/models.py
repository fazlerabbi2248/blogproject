from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class PostModel(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,auto_now_add=False)

    class Meta:
        ordering = ('-date_created',)

    def comment_count(self):
        return self.comment_set.all().count()

    def comments(self):
        return self.comment_set.all()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True,auto_now_add=False)

    def __str__(self):
        return self.content
