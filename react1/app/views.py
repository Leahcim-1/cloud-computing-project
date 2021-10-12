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

from web3 import Web3, HTTPProvider

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


class ethShow(View):
    TEMPLATE = 'Ethshow.html'
    def get(self, request):
        #ETH stuffs
        infura_url = "https://mainnet.infura.io/v3/686d75be8bf046229804af38cfab9505"
        web3 = Web3(Web3.HTTPProvider(infura_url))
        balance = web3.eth.getBalance("0xc8F595E2084DB484f8A80109101D58625223b7C9")
        abi = [{"constant":True,"inputs":[],"name":"mintingFinished","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"unpause","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"}],"name":"mint","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"finishMinting","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":False,"inputs":[],"name":"pause","outputs":[{"name":"","type":"bool"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},{"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_amount","type":"uint256"},{"name":"_releaseTime","type":"uint256"}],"name":"mintTimelocked","outputs":[{"name":"","type":"address"}],"payable":False,"type":"function"},{"constant":True,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":False,"type":"function"},{"constant":False,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":False,"type":"function"},{"anonymous":False,"inputs":[{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":False,"inputs":[],"name":"MintFinished","type":"event"},{"anonymous":False,"inputs":[],"name":"Pause","type":"event"},{"anonymous":False,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"owner","type":"address"},{"indexed":True,"name":"spender","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"name":"from","type":"address"},{"indexed":True,"name":"to","type":"address"},{"indexed":False,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]
        address = "0xd26114cd6EE289AccF82350c8d8487fedB8A0C07"
        contract = web3.eth.contract(address=address, abi=abi)
        totalSupply = contract.functions.totalSupply().call()

        return render(request, self.TEMPLATE,
        {
        "blockNum":web3.eth.blockNumber,
        "balance":web3.fromWei(balance, "ether"), 
        "totalSupply":web3.fromWei(totalSupply, 'ether'),
        "tokenSymbol":contract.functions.name().call()})