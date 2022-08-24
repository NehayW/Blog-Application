from django.test import TestCase
from post.models import PostModel, CommentOnPost, ReplyOnComment
from account.models import User
from datetime import datetime

class TestPostModel(TestCase):
    def setUp(self):
        create_data = User.objects.create(first_name="djbfgddxln", 
                            last_name="any thing",
                            email="email@gmail.com",
                            date_joined=datetime.now())
        user_post = PostModel.objects.create(user=create_data,
                                             description="This is new Post",
                                             post_image="image.jpg")
        
    def test_post_model(self):
        user_post = PostModel.objects.all().first()
        self.assertEqual(user_post.description, "This is new Post")
        self.assertEqual(user_post.post_image,"image.jpg")


class TestCommentModel(TestCase):
    def setUp(self):
        create_data = User.objects.create(first_name="djbfgddxln", 
                            last_name="any thing",
                            email="email@gmail.com",
                            date_joined=datetime.now())
        user_post = PostModel.objects.create(user=create_data,
                                             description="This is new Post",
                                             post_image="image.jpg")
        comment = CommentOnPost.objects.create(post=user_post, 
                                               user=create_data,
                                               comment="nice post")
    
    def test_comment_model(self):
        comment = CommentOnPost.objects.first()
        self.assertEqual(comment.comment,"nice post")


class TestReplyModel(TestCase):
    def setUp(self):
        create_data = User.objects.create(first_name="djbfgddxln", 
                            last_name="any thing",
                            email="email@gmail.com",
                            date_joined=datetime.now())
        user_post = PostModel.objects.create(user=create_data,
                                             description="This is new Post",
                                             post_image="image.jpg")
        comment = CommentOnPost.objects.create(post=user_post, 
                                               user=create_data,
                                               comment="nice post")

        reply_comment = ReplyOnComment.objects.create(re_comment=comment,
                                                      user=create_data,
                                                      reply="reply on comment")
    
    def test_reply_comment(self):
        reply_comment = ReplyOnComment.objects.first()
        self.assertEqual(reply_comment.reply, "reply on comment")