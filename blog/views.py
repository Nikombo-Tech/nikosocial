from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your views here.
@login_required
def home(request):
    form = User.objects.all()
    context = {"form": form}
    return render(request, 'home.html', context)

def register_view(request):
    username = request.POST.get('username')
    first_name = request.POST.get('firstname')  # Corrected field name
    last_name = request.POST.get('lastname')    # Corrected field name
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    email = request.POST.get('email')

    if request.method == 'POST':
        if password1 == password2:
            # Save the user to the database with correct field names
            User.objects.create_user(username=username, first_name=first_name, last_name=last_name, password=password1, email=email)
            return redirect('login')
        else:
            return render(request, 'register.html', {'error': 'Passwords do not match.'})
        
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        # Here you would typically check the credentials against the database
        # For simplicity, we are using Django's built-in authentication system
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        # Here you would typically check the credentials against the database
        # For simplicity, we are using Django's built-in authentication system
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials.'})
        
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    # Here you would typically log the user out of the system
    return redirect('login')

def profile_view(request):
    try:
        user_profile = Profile.objects.get(user=request.user)
    except ObjectDoesNotExist:
        user_profile = Profile.objects.create(user=request.user)

    user_data = request.user  # Use the authenticated user object directly

    if request.method == 'POST':
        # Get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')
        image = request.FILES.get('image')

        # Update user fields
        user_data.username = username
        user_data.email = email
        user_data.first_name = first_name
        user_data.last_name = last_name
        user_data.save()

        # Update profile fields
        user_profile.bio = bio
        if image:
            user_profile.image = image
        user_profile.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('profile')

    context = {
        'user_profile': user_profile,
        'user': user_data,
    }

    return render(request, 'profile.html', context)


from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def post_list_view(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch all posts, ordered by creation date
    return render(request, 'post_list.html', {'posts': posts})

@login_required
def post_detail_view(request, slug):
    post = get_object_or_404(Post, slug=slug)  # Fetch a single post by its slug
    return render(request, 'post_detail.html', {'post': post})

@login_required
def post_create_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')

        # Create a new post
        Post.objects.create(author=request.user, title=title, content=content, image=image)
        return redirect('post_list')  # Redirect to the post list view

    return render(request, 'post_create.html')

@login_required
def post_delete_view(request, slug):
    post = get_object_or_404(Post, slug=slug)

    # Ensure only the author can delete the post
    if post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")

    post.delete()
    return redirect('post_list')

@login_required
def comment_create_view(request, post_slug):
    post = get_object_or_404(Post, slug=post_slug)  # Fetch the post to which the comment belongs

    if request.method == 'POST':
        content = request.POST.get('content')

        # Create a new comment
        Comment.objects.create(post=post, author=request.user, content=content)
        return redirect('post_detail', slug=post.slug)  # Redirect to the post detail view

    return HttpResponseForbidden("Invalid request method.")

@login_required
def comment_delete_view(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)  # Fetch the comment by its ID

    # Ensure only the author of the comment or the post author can delete the comment
    if comment.author != request.user and comment.post.author != request.user:
        return HttpResponseForbidden("You are not allowed to delete this comment.")

    comment.delete()
    return redirect('post_detail', slug=comment.post.slug)  # Redirect to the post detail view