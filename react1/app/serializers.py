from rest_framework import serializers
from .models import CustomUser, Address, Project, UserProject
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        query = UserProject.objects.filter(user=instance)
        ret['project'] = query[0].project.id if len(query) else None
        return ret


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        query = UserProject.objects.filter(project=instance)
        ret['users'] = [userProject.user.id for userProject in query]
        return ret
