from django.core.management.base import BaseCommand
from EasyfoodApp.models import Product
import os
import json


class Command(BaseCommand):
    def handle(self,*args, **kwargs):
        Product.objects.all().delete()

        json_file_path = 'EasyfoodApp/management/commands/db.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            products = json.load(file)
        
        for i in range(len(products)):
            product = products[i]
            exist = Product.objects.filter(title = product['title']).first()
            if not exist:
                Product.objects.create(title = product['title'],
                                        description = product['description'],
                                        image = product['image'],
                                        price = product['price'],
                                        sys_description = product['sys_description'])
