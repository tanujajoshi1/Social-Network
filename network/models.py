from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Profile(models.Model):
	person=models.ForeignKey('User',on_delete=models.CASCADE,related_name='person')
	follower=models.ForeignKey('User',on_delete=models.CASCADE,related_name='follower')



class Post(models.Model):
	user=models.ForeignKey('User',on_delete=models.CASCADE,related_name='creator')
	postBody=models.CharField(max_length=300)
	date=models.DateTimeField(default=timezone.now)
	likes=models.ManyToManyField('User',default=None,blank=True, related_name='likes')

	@property
	def number_of_likes(self):
		return self.likes.all().count()
	


class Like(models.Model):
	user=models.ForeignKey('User',on_delete=models.CASCADE)
	post=models.ForeignKey('Post',on_delete=models.CASCADE)

	def __str__(self):
		return str(self.post)