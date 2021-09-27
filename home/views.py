from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.generic import View


def home(request):
    return render(request, 'home/home.html')


def my_logout(request):
    logout(request)
    return redirect('home')


class Cookie(View):

    def get(self, request, *args, **kwargs):
        # LENDO E SETANDO COOKIES COM DJANGO
        return render(request, 'home/cookie.html')
