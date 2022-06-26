from django.db import models
from login_register_app .models import User 
# Create your models here.

class BookManager(models.Manager):
    def validBook (self,post):
        error = {}
        try:
            if len(post['title'])<=0:
                error['title'] = 'title required..'
        except:
            error['title'] = 'title required..'
        
        try:
            if len(post['desc'])<5 :
                error['desc'] = 'description is less than 5 characters.'
        except:
            error['desc'] = 'description is required'
        return error

class Book(models.Model):
    title = models.CharField(max_length=100)
    uploaded_by = models.ForeignKey(User,related_name='uploaded_books',blank=False,on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User,related_name='liked_books')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    desc = models.TextField()
    objects = BookManager()