"""nexus_wallet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from identification import views

urlpatterns = [

    path('', views.home , name='home'),

    #authentication
    path('login/', views.loginuser, name='loginuser'),
    path('signup/', views.signupuser, name='signupuser'),
    path('current/', views.currentuser, name='currentuser'),
    path('current/agent/', views.agent, name='agent'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('update/', views.updateprofile, name='updateprofile'),

    #ACCOUNT
    path('account/',views.accountinfo , name='accountinfo'),
    path('paybill/',views.billpayment , name='billpayment'),
    path('sendmoney/',views.moneysending , name='moneysending'),
    path('cashout/',views.pulloutmoney , name='pulloutmoney'),
    path('receipt/',views.showreceipts , name='showreceipts'),
    path('cashin/',views.cashin , name='cashin'),
    path('paybill/electricity/',views.electricitybill , name='electricitybill'),
    path('paybill/gas/',views.gasbill , name='gasbill'),
    path('paybill/water/',views.waterbill , name='waterbill'),
    path('paybill/phone/',views.phonebill , name='phonebill'),
    path('paybill/internet/',views.internetbill , name='internetbill'),
    path('paybill/bill/<int:bill_pk>',views.billform , name='billform'),
    path('add/',views.addmoney , name='addmoney'),
    path('add/creditcard/',views.card , name='card'),
    path('add/bank/',views.netbank , name='netbank'),

]
