from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def gl(request):
    return render(request, 'gl.html')

def logout(request):
    return render(request, 'home.html')