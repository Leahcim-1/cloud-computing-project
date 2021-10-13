from django.urls import path
from .views import UserList, UserDetail

urlpatterns = [
    path('users/', UserList.as_view(), name="user_list"),
    path('users/<int:pk>/', UserDetail.as_view(), name="user_detail")
    # path('', mainPage.as_view(), name='mainPage'),
    # path('showall', showAllPage.as_view(), name='showAll'),
    # path('add/<str:name>/<int:price>', add.as_view(), name='adds'),
    # path('regist', Regist.as_view(), name='regist'),
    # path('login', Login.as_view(), name='login'),
    # path('logout', Logout.as_view(), name='logout'),
    # path('apage', Apage.as_view(), name='Apage'),
    # path('ethshow', ethShow.as_view(), name='ethShow')
] 