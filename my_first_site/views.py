from django.http import HttpResponse
from django.shortcuts import render
def get_blog(request):
    return render(request ,'base.html')