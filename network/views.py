from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.shortcuts import render,get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator
from django import forms
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import User,Profile,Post,Like


def index(request):
    posts=Post.objects.all().order_by('id').reverse()
    paginator=Paginator(posts,10)
    pageNumber=request.GET.get('page')
    pageObject=paginator.get_page(pageNumber)
    return render(request, "network/index.html",{'pageObject':pageObject})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


class Edit(forms.Form):
    #widget is django's represenTATION Of html input element
    #widget.attrs is specifying the 'type' attribute to take use HTML5 input types
    text=forms.CharField(widget=forms.Textarea(attrs={'class':'form-control'}),label='')


@login_required
def edit(request,postID):
    postObject=Post.objects.get(pk=postID)    
    if request.method=='GET':
        if postObject.user==request.user:        #checks if no other user can edit anyone's post
            return render(request,'network/edit.html',{
                'postID':postID,
                'edit':Edit(initial={'text':postObject.postBody})
                })
        else:
            return HttpResponse(f"Unknown / Unauthorised user")
    else:        
        form=Edit(request.POST)
        if form.is_valid():
            text=form.cleaned_data["text"]
            postObject.postBody=text
            postObject.save()
            return HttpResponseRedirect(reverse('index'))



def like(request):
    user=request.user
    
    if request.method=='GET':
        postID=request.GET['postID']
        postLiked=Post.objects.get(pk=postID)
        #Removing like
        if user in postLiked.likes.all():
            postLiked.likes.remove(user)
            Like.objects.get(post=postLiked,user=user).delete()            
        #Adding like
        else:
            like=Like.objects.get_or_create(post=postLiked,user=user)
            postLiked.likes.add(user)
            postLiked.save()
        return HttpResponse('Success')


def create(request,username):
    if request.method=='GET':
        user=get_object_or_404(User,username=username)
        return render(request,"network/create.html",{'user':user})
    else:
        user=get_object_or_404(User,username=username)
        text=request.POST["text"]
        post=Post.objects.create(postBody=text,user=user)
        post.save()
        return HttpResponseRedirect(reverse('index'))


def following(request,username):
    if request.method=='GET':
        presentUser=get_object_or_404(User,username=username)
        fobj=Profile.objects.filter(follower=presentUser)
        posts=Post.objects.all().order_by('id').reverse()
        presentPosts=[]
        for i in posts:
            for follower in fobj:
                if follower.person==i.user:
                    presentPosts.append(i)
        if not fobj:

            return render(request,'network/following.html',{'message':"No following"})

        paginator=Paginator(presentPosts,10)
        pageNumber=request.GET.get('page')
        pageObject=paginator.get_page(pageNumber)

        return render(request,'network/following.html',{'pageObject':pageObject})


def profile(request,username):
    presentUser=request.user
    profileuser=get_object_or_404(User,username=username)
    posts=Post.objects.filter(user=profileuser).order_by('id').reverse()
    totalposts=len(posts)

    
    if request.method=='GET':
        presentUser=request.user
        profileuser=get_object_or_404(User,username=username)
        posts=Post.objects.filter(user=profileuser).order_by('id').reverse()
        follower=Profile.objects.filter(person=profileuser)
        following=Profile.objects.filter(follower=profileuser)
        if request.user.is_anonymous:
            return HttpResponseRedirect(reverse('login'))
        else:
            follow=Profile.objects.filter(follower=presentUser,person=profileuser)
            totalFollowers=len(follower)
            totalFollowings=len(following)
            

            paginator=Paginator(posts,10)
            pageNumber=request.GET.get('page')
            pageObject=paginator.get_page(pageNumber)

            return render(request,'network/profile.html',{
                'profileuser':profileuser,
                'pageObject':pageObject,
                'follower':totalFollowers,
                'following':totalFollowings,
                'follow':follow,
                'postcount':totalposts

                })
    else:

        follow=Profile.objects.filter(follower=request.user, person=profileuser)

        paginator=Paginator(posts,10)
        pageNumber=request.GET.get('page')
        pageObject=paginator.get_page(pageNumber)

        if not follow:
            followObject=Profile.objects.create(person=profileuser,follower=presentUser)
            followObject.save()
            follower=Profile.objects.filter(person=profileuser)
            following=Profile.objects.filter(follower=profileuser)
            follow=Profile.objects.filter(follower=request.user,person=profileuser)
            
            totalFollowers=len(follower)
            totalFollowings=len(following)

            return render(request,"network/profile.html",{
                'profileuser':profileuser,
                'pageObject':pageObject,
                'follower':totalFollowers,
                'following':totalFollowings,
                'follow':follow,
                'postcount':totalposts
                })

        else:
            follow.delete()
            follower=Profile.objects.filter(person=profileuser)
            following=Profile.objects.filter(follower=profileuser)
            
            totalFollowers=len(follower)
            totalFollowings=len(following)

            return render(request,"network/profile.html",{
                'profileuser':profileuser,
                'pageObject':pageObject,
                'follower':totalFollowers,
                'following':totalFollowings,
                'follow':follow,
                'postcount':totalposts
                })
