from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from .forms import BlogPostForm
from django.http import JsonResponse
from .models import *
import json
from django.core import serializers
from firebase_admin.messaging import Message
from fcm_django.models import FCMDevice
from core.messages import Message as ms

# Create your views here.

class PostBlog(View):
    def post(self, request):

        form = BlogPostForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()
            messages.add_message(request, 
                                 messages.SUCCESS, 
                                 ms.POST_CREATEd)
            return redirect('/')
        else:
            print(form.errors)
            messages.add_message(request, 
                                 messages.ERROR, 
                                 ms.POST_NOT_CREATED)
            return redirect('/')
      

class LikePost(View):

    def get(self, request, pk):

        blog = PostModel.objects.filter(id=pk).first()
        if not blog.like.filter(id=request.user.id):
            blog.like.add(request.user)
            message_obj = Message(
                data={
                    "title" : "Like",
                    "body" : "like your post",
                },
            )
            try:
                if request.user != blog.user:
                    device = FCMDevice.objects.filter(user=blog.user, 
                                                        active=True).last()
                    device.send_message(message_obj)
                else:
                    pass
            except:
                pass
            like = blog.like.all().count()
            dislike = blog.dislike.all().count()
            if blog.dislike.filter(id=request.user.id):
                blog.dislike.remove(request.user)
                like = blog.like.all().count()
                dislike = blog.dislike.all().count()
                return JsonResponse({"like": like, "dislike": dislike})
            return JsonResponse({"like": like, "dislike": dislike})
        else:
            blog.like.remove(request.user)
            like = blog.like.all().count()
            dislike = blog.dislike.all().count()                
            return JsonResponse({"like": like, "dislike": dislike})


class DislikePost(View):

    def get(self, request, pk):

        blog = PostModel.objects.filter(id=pk).first()
        if not blog.dislike.filter(id=request.user.id):
            blog.dislike.add(request.user)
            like = blog.like.all().count()
            message_obj = Message(
                data={
                    "title" : "Dislike",
                    "body" : "Dislike your post",
                },
            )
            try:
                if request.user != blog.user:
                    device = FCMDevice.objects.filter(user=blog.user, 
                                                        active=True).last()
                    device.send_message(message_obj)
                else:
                    pass
            except:
                pass
            dislike = blog.dislike.count()     
            if blog.like.filter(id=request.user.id):
                blog.like.remove(request.user)
                like = blog.like.count()
                dislike = blog.dislike.count()
                return JsonResponse({"like": like, "dislike": dislike})
            return JsonResponse({"like": like, "dislike": dislike})
        else:
            blog.dislike.remove(request.user)
            like = blog.like.all().count()
            dislike = blog.dislike.all().count()                
            return JsonResponse({"like": like, "dislike": dislike})


class MyPost(View):
    def get(self, request):
        blogs = PostModel.objects.filter(user=request.user)
        return render(request, 'mypost.html', {"posts":blogs})


class DeletePost(View):
    def get(self, request, pk):
        if request.user.is_authenticated and \
            request.user == PostModel.objects.filter(id=pk).first().user:
            blogs = PostModel.objects.filter(user=request.user)
            PostModel.objects.filter(id=pk).delete()
            messages.add_message(request, messages.SUCCESS, ms.POST_DELETED)
            return redirect("mypost")
        else:
            return redirect('mypost')


class PostComment(View):

    def post(self, request):

        data = request.POST
        post = PostModel.objects.filter(id=data['pk']).first()
        comment = CommentOnPost.objects.create(comment=data['comment'],
                                                user=request.user,
                                                post=post)
        message_obj = Message(
            data={
                "title" : "Commented",
                "body" : comment.comment[:50:],
            },
        )
        try:
            if request.user != post.user:
                device = FCMDevice.objects.filter(user=post.user, 
                                                    active=True).last()
                device.send_message(message_obj)
            else:
                pass
        except:
            pass
        your_comment = {}
        your_comment["id"] = comment.id
        your_comment["post_id"] = comment.post.id
        your_comment["user_name"] = comment.user.first_name
        your_comment["profile_image"] = comment.user.profile_image.url
        your_comment["comment"] = comment.comment
        your_comment["time"] = comment.commented_at
        comments = PostModel.objects.filter(id=data['pk']).first()
        comments = comments.post.all().count()
        
        return JsonResponse({"message":ms.COMMENT,
                                "comments": comments,
                                "your_comment":your_comment})

class ReplyCommentView(View):

    def post(self, request):
        data = request.POST
        comment = CommentOnPost.objects.filter(id=data['pk']).first()
        reply_comment = ReplyOnComment.objects.create(reply=data['reply'],
                                                        user=request.user,
                                                        re_comment=comment)
        message_obj = Message(
            data={
                "Nick" : "You Got Reply",
                "body" : reply_comment.reply,
            },
        )
        try:
            if request.user != comment.user:
                device = FCMDevice.objects.filter(user=comment.user, 
                                                    active=True).last()
                device.send_message(message_obj)
            else:
                pass
        except:
            pass

        user_reply = {}
        user_reply['comment_id'] = reply_comment.re_comment.id
        user_reply['user_name'] = reply_comment.user.first_name
        user_reply['reply'] = reply_comment.reply
        user_reply['time'] = reply_comment.commented_at
        user_reply['profile_image'] = reply_comment.user.profile_image.url            
        return JsonResponse({"message":ms.REPLY, 
                                "user_reply":user_reply})

            