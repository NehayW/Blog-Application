from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('postblog/', login_required(views.PostBlog.as_view()), 
                                                     name="blogpost"),
    path('likepost/<int:pk>/',login_required(views.LikePost.as_view()),
                                                      name="likepost"),
    path('dislikepost/<int:pk>/', login_required(views.DislikePost.as_view()),
                                                    name="dislikepost"),
    path('my-post/', login_required(views.MyPost.as_view()), name="mypost"),
    path('delete-post/<int:pk>', views.DeletePost.as_view(), 
                                                    name="delete-post"),
    path('post-comment/', login_required(views.PostComment.as_view()), 
                                         name="postcomment"),
    path('reply-comment/', login_required(views.ReplyCommentView.as_view()), 
                                                    name="replycomment")
]