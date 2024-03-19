
from django.shortcuts import render


def testView(request):

    p_name = "EASYFOOD"

    return render(request, "test_template.html", {"project_name": p_name })
