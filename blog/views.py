from django.shortcuts import render
from .models import *
from django.views.generic import View
from django.shortcuts import get_object_or_404
from .utils import ObjectDetailMixin
from .forms import *
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q


def posts_list(request):
    posts=Post.objects.all()
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(title__icontains=search_query) | Q(body__icontains=search_query))
    else:
        posts = Post.objects.all()
    return render(request,'blog/index.html',context={'posts':posts})


class PostDetail(ObjectDetailMixin, View):
    model=Post
    template= 'blog/post_detail.html'


def tags_list(request):
    tags=Tag.objects.all()
    return render(request,'blog/tags_list.html',context={'tags':tags})

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template =  'blog/tag_detail.html'

class TagCreate(View):
    def get(self,request):
        form=TagForm
        return render(request, 'blog/tag_create.html',context={'form':form})

    def post(self,request):
        bound_form=TagForm(request.POST)

        if bound_form.is_valid():
            new_tag=bound_form.save()
            return redirect(new_tag)

        return render(request,'blog/tag_create.html', context={'form':bound_form})


class PostCreate(View):
    def get(self,request):
        form=PostForm
        return render(request, 'blog/post_create.html',context={'form':form})

    def post(self,request):
        bound_form=PostForm(request.POST)

        if bound_form.is_valid():
            new_post=bound_form.save()
            return redirect(new_post)

        return render(request,'blog/post_create.html', context={'form':bound_form})

class TagUpdate(View):
    def get(self,request,slug):
        tag=Tag.objects.get(slug__iexact=slug)
        bound_form=TagForm(instance=tag)
        return render(request,'blog/tag_update_form.html',context={'form':bound_form,'tag':tag})


    def post(self, request,slug):
        tag=Tag.objects.get(slug__iexact=slug)
        bound_form = TagForm(request.POST,instance=tag)

        if bound_form.is_valid():
            new_tag = bound_form.save()
            return redirect(new_tag)
        return render(request, 'blog/tag_update_form.html', context={'form': bound_form,'tag':tag})

class PostUpdate(View):
    def get(self,request,slug):
        post=Post.objects.get(slug__iexact=slug)
        bound_form=PostForm(instance=post)
        return render(request,'blog/post_update_form.html',context={'form':bound_form,'post':post})


    def post(self, request,slug):
        post=Post.objects.get(slug__iexact=slug)
        bound_form = PostForm(request.POST,instance=post)

        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        return render(request, 'blog/post_update_form.html', context={'form': bound_form,'post':post})

class TagDelete(View):
    def get(self,request,slug):
        tag=Tag.objects.get(slug__iexact=slug)
        return render(request,'blog/tag_delete_form.html',context={'tag':tag})


    def post(self, request, slug):
          tag = Tag.objects.get(slug__iexact=slug)
          tag.delete()
          return redirect(reverse('tags_list_url'))

class PostDelete(View):
    def get(self,request,slug):
        post=Post.objects.get(slug__iexact=slug)
        return render(request,'blog/post_delete_form.html',context={'post':post})


    def post(self, request, slug):
          post = Post.objects.get(slug__iexact=slug)
          post.delete()
          return redirect(reverse('posts_list_url'))
