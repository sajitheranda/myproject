from django.shortcuts import render

# Create your views here.


def post_list(request):
    post="post"
    return render(request, 'post_list.html', {'posts': post})