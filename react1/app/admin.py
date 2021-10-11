from django.contrib import admin
from .models import Transactions
from django.utils.html import format_html


class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'time', 'return_href']
    list_filter=('name', )
    search_fields=['content']
    ordering=['-id']
    list_per_page=5

    def return_href(self, obj):
        return format_html(
        '<a href="https://www.google.com/">Google Link</a>')

admin.site.register(Transactions, TransactionsAdmin) 