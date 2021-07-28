from .models import BlogModel,CommentModel
from .forms import SearchForm,CommentForm
from django.shortcuts import render,redirect
from django.http import Http404

def BlogListView(request):
    dataset = BlogModel.objects.all()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            blog = BlogModel.objects.get(blog_title=title)
            return redirect(f'/blog/{blog.id}')
        else:
            form = SearchForm()
            context = {
                'dataset':dataset,
                'form':form,
                }
    else:
        return render(request,'blogapp/signin.html')

    return render(request,'blogapp/listview.html',context)
 
 
def BlogDetailView(request,_id):
    try:
        data =BlogModel.objects.get(id =_id)
        comments = CommentModel.objects.filter(blog = data)
    except BlogModel.DoesNotExist:
        raise Http404('Data does not exist')
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment = CommentModel(your_name= form.cleaned_data['your_name'],
            comment_text=form.cleaned_data['comment_text'],
            blog=data)
            Comment.save()
            return redirect(f'/blog/{_id}')
    else:
        form = CommentForm()
 
    context = {
            'data':data,
            'form':form,
            'comments':comments,
        }
    return render(request,'blogapp/detailview.html',context)

###########################################################################
# urls.py 
from django.contrib import admin
from django.urls import path
from .views import *
 
urlpatterns = [
    path('blogs/', BlogListView, name='blogs'),
    path('blog/<int:_id>', BlogDetailView, name='blog'),
  
###########################################################################
# models.py
from django.db import models


class BlogModel(models.Model):
    id = models.IntegerField(primary_key=True)
    blog_title = models.CharField(max_length=20)
    blog = models.TextField()
 
    def __str__(self):
        return f"Blog: {self.blog_title}"
 
class CommentModel(models.Model):
    your_name = models.CharField(max_length=20)
    comment_text = models.TextField()
    blog = models.ForeignKey('BlogModel', on_delete=models.CASCADE)
     
    def __str__(self):
        return f"Comment by Name: {self.your_name}"
  
 ###########################################################################
 # forms.py
  from django import forms
 
class CommentForm(forms.Form):
    your_name =forms.CharField(max_length=20)
    comment_text =forms.CharField(widget=forms.Textarea)
 
    def __str__(self):
        return f"{self.comment_text} by {self.your_name}"
 
 
 
class SearchForm(forms.Form):
    title = forms.CharField(max_length=20)
  
############################################################################
# Admin.py 
from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.BlogModel)
admin.site.register(models.CommentModel)
