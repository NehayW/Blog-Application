from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('postblog/', views.PostBlog.as_view(), 
                                                     name="blogpost"),
    path('likepost/<int:pk>/', views.LikePost.as_view(),
                                                      name="likepost"),
    path('dislikepost/<int:pk>/', views.DislikePost.as_view(),
                                                    name="dislikepost"),
    path('my-post/', views.MyPost.as_view(), name="mypost"),
    # path('update-post/<int:pk>', views.UpdatePost.as_view(), name="update-post"),
    path('delete-post/<int:pk>', views.DeletePost.as_view(), 
                                                    name="delete-post"),
    path('post-comment/', views.PostComment.as_view(), name="postcomment"),
    path('reply-comment/', views.ReplyCommentView.as_view(), 
                                                    name="replycomment")
]