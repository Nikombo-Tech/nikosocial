from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify
from django.urls import reverse

class User(AbstractUser):
    ROLE_CHOICES = [
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
        ('Admin', 'Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Student')

    def __str__(self):
        return f"{self.username} ({self.role})"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Link to the Post
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')  # Link to the User
    content = models.TextField()  # The comment content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the comment is created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the comment is updated

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"