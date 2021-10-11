from django.db import models
import time
# Create your models here.

class Transactions(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return 'name:{}'.format(self.name)

class Apage(models.Model):
    title=models.CharField(max_length=10)

    def _str_(self):
        return '{}'.format(self.title)
    
    class Meta:
        permissions =[
            ('look_a_page', 'can get this page')
        ]