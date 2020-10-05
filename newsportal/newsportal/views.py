
from django.contrib.auth import authenticate, login ,logout
from django.http import HttpResponse
from django.shortcuts import render ,redirect,get_object_or_404
from blog.models import Blog
from django.contrib.auth.models import User
from django.contrib import messages
from blog.forms import  BlogForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
def about(request):
    return render(request, 'about.html')


def home(request):
    data =Blog.objects.all()
    context = {
        'blog': data
    }
    return render(request, 'home.html', context)


def views_more(request, id):
    data = get_object_or_404(Blog,pk=id)
    context = {
        'blog': data
    }

    return render(request, 'view_more.html', context)


def signup(request):
    if request.method == "GET":
        return render(request, 'signup.html')
    else:
        u = request.POST['username']
        e = request.POST['email']
        p1 = request.POST['pass']
        p2 = request.POST['pass1']
        if p1 == p2:
            try:

              u = User(username=u, email=e)
              u.set_password(p1)
              u.save()
            except:
              messages.add_message(request,messages.ERROR,"Username already exists")
              return redirect('signup')
            messages.add_message(request, messages.SUCCESS, "password match sucessful")
            return redirect("signin")

        else:
            messages.add_message(request, messages.ERROR, "password doesnot match")
            return redirect("signup")


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        u = request.POST['username']
        p = request.POST['pass']
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.add_message(request, messages.ERROR, "Not logged in")
            return redirect('signin')


def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def dashboard(request):
    data=Blog.objects.all()[::-1]
    context={
        'blog': data
    }

    return render(request, 'dashboard.html',context)


def create_post(request):
    form = BlogForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, "Created sucessfully")
        return redirect('dashboard')
    context = {
        'form': form
    }
    return render(request, 'create_post.html', context)
def edit_post(request,id):
    data = Blog.objects.get(pk=id)
    form = BlogForm(request.POST or None, request.FILES or None,instance=data)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, "Edited sucessfully")
        return redirect('dashboard')
    context = {
        'form': form
    }
    return render(request, 'edit_post.html', context)

def deletepost(request,id):
    b=Blog.objects.get(pk=id)
    b.delete()
    messages.add_message(request, messages.SUCCESS, "delete sucessfully")
    return redirect('dashboard')
