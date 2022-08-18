from django.db import models
from account.models import User
# Create your models here.

class PostModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name="user")
    description = models.TextField()
    post_image = models.ImageField(upload_to='media/image/post', null=True,
                                    blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like = models.ManyToManyField(User, related_name="like" ,blank=True)
    dislike = models.ManyToManyField(User, related_name="dislike", blank=True)

    def __str__(self):
        return self.user.email


class CommentOnPost(models.Model):
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE, 
                                        related_name="post")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post.user.email
  

class ReplyOnComment(models.Model):
    re_comment = models.ForeignKey(CommentOnPost, on_delete=models.CASCADE,
                                                related_name="re_comment")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    commented_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.re_comment.post.user.email

