from django.shortcuts import render

# Create your views here.




def post_list(request):
    post="post"
    return render(request, 'post_list.html', {'posts': post})

def custom_page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

def custom_500_view(request):
    return render(request, '500.html', status=500)
