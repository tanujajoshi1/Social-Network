from django.contrib import admin
from .models import Profile,User,Like,Post

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Post)