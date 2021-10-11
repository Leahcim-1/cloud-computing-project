from django.urls import path
from .views import showAllPage,add,Regist,Login,Logout,Apage,mainPage

urlpatterns = [
    path('', mainPage.as_view(), name='mainPage'),
    path('showall', showAllPage.as_view(), name='showAll'),
    path('add/<str:name>/<int:price>', add.as_view(), name='adds'),
    path('regist', Regist.as_view(), name='regist'),
    path('login', Login.as_view(), name='login'), 
    path('logout', Logout.as_view(), name='logout'),
    path('apage', Apage.as_view(), name='Apage')
] 