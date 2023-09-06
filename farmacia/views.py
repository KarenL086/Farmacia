from django.shortcuts import render

def inicioAdmin(request):
    return render(request, 'inicioAdmin.html',{})
def inicio(request):
    return render(request, 'inicio.html',{})
def login(request):
    return render(request, 'login.html',{})