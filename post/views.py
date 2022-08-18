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

# Create your views here.

class PostBlog(View):
    def post(self, request):
        if request.user.is_authenticated:
            form = BlogPostForm(request.POST, request.FILES)
            print(form)
            if form.is_valid():
                form = form.save(commit=False)
                form.user = request.user
                # form.post_image = request.POST['post_image']
                form.save()
                messages.add_message(request, messages.SUCCESS, 
                                     "Post submited")
                return redirect('/')
            else:
                print(form.errors)
                messages.add_message(request, messages.ERROR, 
                                     "Post not done")
                return redirect('/')
        else:
            return redirect("login")       

class LikePost(View):

    def get(self, request, pk):
        if request.user.is_authenticated:
            blog = PostModel.objects.filter(id=pk).first()
            if not blog.like.filter(id=request.user.id):
                blog.like.add(request.user)
                message_obj = Message(
                    data={
                        "title" : "Like",
                        "body" : "like your post",
                        "Room" : "PortugalVSDenmark"
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
        else:
            return JsonResponse({"message":"login first"})


class DislikePost(View):

    def get(self, request, pk):
        if request.user.is_authenticated:
            blog = PostModel.objects.filter(id=pk).first()
            if not blog.dislike.filter(id=request.user.id):
                blog.dislike.add(request.user)
                like = blog.like.all().count()
                message_obj = Message(
                    data={
                        "title" : "Dislike",
                        "body" : "Dislike your post",
                        "Room" : "PortugalVSDenmark"
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
        else:
            return JsonResponse({"message":"login first"})


class MyPost(View):
    def get(self, request):
        if request.user.is_authenticated:
            blogs = PostModel.objects.filter(user=request.user)
            return render(request, 'mypost.html', {"posts":blogs})
        else:
            return redirect("/")


# class UpdatePost(View):
#     def get(self, request, pk):
#         if request.user.is_authenticated and request.user == PostModel.objects.filter(id=pk).first().user:
#             blogs = PostModel.objects.filter(user=request.user)
#             update = PostModel.objects.filter(id=pk).first()
#             return render(request, 'mypost.html', {"posts":blogs, 
#                                                     "update":update})
#         else:
#             messages.add_message(request, messages.WARNING, "You are Not autherize for update this post")
#             return redirect("mypost")
#     def post(self, request, pk):
#         data = request.POST
#         import pdb; pdb.set_trace()
#         if request.user.is_authenticated and request.user == PostModel.objects.filter(id=data['pk']).first().user:
#             blog = PostModel.objects.filter(id=data['pk'])
#             form = BlogPostForm(request.POST, instance=blog)
#             if form.is_valid():
#                 form = form.save(commit=False)
#                 form.post_image = data['post_image']
#                 form.save()
#                 messages.add_message(request, messages.SUCCESS, "Post Updated")
#                 return redirect('mypost')
#             else:
#                 messages.add_message(request, messages.SUCCESS, "Invalid form")
#                 return redirect("mypost")
#         return redirect("mypost")



class DeletePost(View):
    def get(self, request, pk):
        if request.user.is_authenticated and \
            request.user == PostModel.objects.filter(id=pk).first().user:
            blogs = PostModel.objects.filter(user=request.user)
            PostModel.objects.filter(id=pk).delete()
            messages.add_message(request, messages.SUCCESS, "Post Deleted")
            return redirect("mypost")
        else:
            return redirect('mypost')


class PostComment(View):

    def post(self, request):
        if request.user.is_authenticated:
            data = request.POST
            post = PostModel.objects.filter(id=data['pk']).first()
            comment = CommentOnPost.objects.create(comment=data['comment'],
                                                    user=request.user,
                                                    post=post)
            message_obj = Message(
                data={
                    "title" : "Commented",
                    "body" : comment.comment[:50:],
                    "Room" : "PortugalVSDenmark"
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
            # import pdb; pdb.set_trace()
            your_comment["profile_image"] = comment.user.profile_image.url
            # print(str(your_comment['profile_image']))
            your_comment["comment"] = comment.comment
            your_comment["time"] = comment.commented_at
            comments = PostModel.objects.filter(id=data['pk']).first()
            comments = comments.post.all().count()
            
            return JsonResponse({"message":"commented on post", 
                                 "comments": comments, 
                                 "your_comment":your_comment})
        else:
            return JsonResponse({"message":"You are not loged in"})


class ReplyCommentView(View):

    def post(self, request):
        if request.user.is_authenticated:
            data = request.POST
            comment = CommentOnPost.objects.filter(id=data['pk']).first()
            reply_comment = ReplyOnComment.objects.create(reply=data['reply'],
                                                          user=request.user,
                                                          re_comment=comment)
            message_obj = Message(
                data={
                    "Nick" : "You Got Reply",
                    "body" : reply_comment.reply,
                    "Room" : "PortugalVSDenmark"
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
            return JsonResponse({"message":"user reply", 
                                 "user_reply":user_reply})

        else:
            return JsonResponse({"message":"login frist"})