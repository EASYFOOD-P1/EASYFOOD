from django.shortcuts import render




def test(request):
    return render(request, "first.html")
# Create your views here.
