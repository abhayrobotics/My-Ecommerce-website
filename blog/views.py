from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogpost

# Create your views here.

def index(request):
    
 
    all_post= Blogpost.objects.all()
 
    print(all_post)
    return render(request,'blog/index.html',{'all_post':all_post})


def blogpost(request,id):
    post = Blogpost.objects.filter(post_id=id)[0]
    # print(post)
    # print(type(post))
    return render(request,'blog/blogpost.html',{'post':post})