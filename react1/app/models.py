from django.db import models


class Address(models.Model):
    streetName = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    countryCode = models.CharField(max_length=50)
    postalCode = models.CharField(max_length=50)


class Project(models.Model):
    description = models.CharField(max_length=100)


class CustomUser(models.Model):
    username = models.CharField(max_length=100)
    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL, related_name="user")


class UserProject(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="user_project")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="user_project")
