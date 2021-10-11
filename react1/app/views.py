from app.models import Transactions, Apage
from datetime import datetime
from rest_framework import viewsets
from .serializers import TransactionSerializer

from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views.generic import View

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Permission
from django.contrib.auth import login, logout, authenticate

# Create your views here.

class mainPage(View):
    def get(self, request):
        return HttpResponse('MainPage')

class add(View):
    def get(self, request, name, price):
        serializer_class = TransactionSerializer
        this_transaction = Transactions.objects.create(
            name=name, price=price)
        return HttpResponse('new transaction created')


class showAllPage(View):
    TEMPLATE = 'showAll.html'
    def get(self, request):
        transactions_all=Transactions.objects.all()
        return render(request, self.TEMPLATE, {"transactions_all": Transactions.objects.all() })


class Regist(View):
    TEMPLATE='regist.html'

    def get(self, request):
        error = request.GET.get('error', '')
        return render(request, self.TEMPLATE, {'error':error})
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        check_password = request.POST.get('check_password')

        if password!=check_password:
            return redirect('/regist?error=different_password_when_entering')
        
        user_exists = User.objects.filter(username=username).exists()
        if user_exists:
            return redirect('/regist?error=existing_user')
        hash_password = make_password(password)
        User.objects.create_user(
            username=username,
            password=hash_password
        )
        #print(username, password, check_password)

        return redirect(reverse('login'))

class Login(View):
    TEMPLATE = 'login.html'

    def get(self, request):
        return render(request, self.TEMPLATE)
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user= authenticate(username=username, password=password)
        if user:
            login(request, user)
        else:
            return redirect("/login?error=login_fail")
        return redirect('/login')

class Logout(View):
    def get(self, request):
        logout(request)

        return redirect(reverse('login'))

class Apage(View):
    TEMPLATE='Apage.html'
    
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse("you do not have access")
        
        a_permission = Permission.objects.get(codename='look_a_page')
        if not request.user.has_perm(a_permission):
            return HttpResponse('you have no permission to visit')
        return render(request, self.TEMPLATE)