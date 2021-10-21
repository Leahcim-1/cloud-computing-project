from rest_framework.response import Response
from .serializers import CustomUserSerializer, AddressSerializer, ProjectSerializer

from rest_framework import generics, status

from .models import CustomUser, Address, Project, UserProject


class UserList(generics.ListCreateAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        user = CustomUser.objects.get(pk=serializer.data['id'])
        if request.data.get('project'):
            project = Project.objects.filter(pk=request.data.get('project'))
            if len(project):
                UserProject.objects.create(user=user, project=project[0])
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()

    def put(self, request, *args, **kwargs):
        return self.patch(request, *args, **kwargs)


class ProjectList(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()

    def get(self, request, *args, **kwargs):
        for project in self.get_queryset():
            query = UserProject.objects.filter(project=project)
            if not len(query):
                project.delete()
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.data
        if 'users' not in data:
            return Response("Please specify user", status=status.HTTP_400_BAD_REQUEST)
        else:
            users = []
            for userID in data['users']:
                query = CustomUser.objects.filter(pk=userID)
                if len(query):
                    existingRelation = UserProject.objects.filter(user=query[0])
                    if existingRelation:
                        return Response("user {} already has project".format(userID), status=status.HTTP_400_BAD_REQUEST)
                    users.append(query[0])
            if len(users) <= 0:
                return Response("Invalid users", status=status.HTTP_404_NOT_FOUND)
            project = Project.objects.create(description=data['description'])
            for user in users:
                UserProject.objects.create(user=user, project=project)
            serializer = self.get_serializer(project)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AddressList(generics.ListCreateAPIView):
    serializer_class = AddressSerializer
    queryset = Address.objects.all()

# class mainPage(View):
#     def get(self, request):
#         return HttpResponse('MainPage')
#
# class add(View):
#     def get(self, request, name, price):
#         serializer_class = TransactionSerializer
#         this_transaction = Transactions.objects.create(
#             name=name, price=price)
#         return HttpResponse('new transaction created')
#
#
# class showAllPage(View):
#     """
#     DESCRIPTION
#     """
#     TEMPLATE = 'showAll.html'
#     def get(self, request):
#         transactions_all=Transactions.objects.all()
#         return render(request, self.TEMPLATE, {"transactions_all": Transactions.objects.all() })
#
#
# class Regist(View):
#     TEMPLATE='regist.html'
#
#     def get(self, request):
#         error = request.GET.get('error', '')
#         return render(request, self.TEMPLATE, {'error':error})
#
#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         check_password = request.POST.get('check_password')
#
#         if password!=check_password:
#             return redirect('/regist?error=different_password_when_entering')
#
#         user_exists = User.objects.filter(username=username).exists()
#         if user_exists:
#             return redirect('/regist?error=existing_user')
#         hash_password = make_password(password)
#         User.objects.create_user(
#             username=username,
#             password=hash_password
#         )
#         #print(username, password, check_password)
#
#         return redirect(reverse('login'))
#
# class Login(View):
#     TEMPLATE = 'login.html'
#
#     def get(self, request):
#         return render(request, self.TEMPLATE)
#
#     def post(self, request):
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user= authenticate(username=username, password=password)
#         if user:
#             login(request, user)
#         else:
#             return redirect("/login?error=login_fail")
#         return redirect('/login')
#
# class Logout(View):
#     def get(self, request):
#         logout(request)
#
#         return redirect(reverse('login'))
#
# class Apage(View):
#     TEMPLATE='Apage.html'
#
#     def get(self, request):
#         if not request.user.is_authenticated:
#             return HttpResponse("you do not have access")
#
#         a_permission = Permission.objects.get(codename='look_a_page')
#         if not request.user.has_perm(a_permission):
#             return HttpResponse('you have no permission to visit')
#         return render(request, self.TEMPLATE)