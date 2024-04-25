from django.core.management.base import BaseCommand
from EasyfoodApp.models import Product
import os
import json
import numpy as np


class Command(BaseCommand):
    def handle(self,*args, **kwargs):
        Product.objects.all().delete()

        json_file_path = 'EasyfoodApp/management/commands/embeddings_db.json'

        with open(json_file_path, 'r', encoding='utf-8') as file:
            products = json.load(file)
        
        for i in range(len(products)):
            product = products[i]
            exist = Product.objects.filter(title = product['title']).first()
            emb = product['embedding']
            emb_binary = np.array(emb).tobytes()
            if not exist:
                Product.objects.create(title = product['title'],
                                        description = product['description'],
                                        emb = emb_binary,
                                        image = product['image'],
                                        price = product['price'],)
