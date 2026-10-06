from django.shortcuts import render


def dashboard(request):
    return render(request, "dashboard.html")

def menu(request):
    return render(request, "menu.html")