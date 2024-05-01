from django.core.management.base import BaseCommand
from EasyfoodApp.models import Product
import json
import os
import numpy as np

class Command(BaseCommand):
    help = 'Modify path of images'

    def handle(self, *args, **kwargs):
        ##Código para leer los embeddings del archivo embeddings_db.json
        json_file_path = 'EasyfoodApp/management/commands/embeddings_db.json'
        # Load data from the JSON file
        with open(json_file_path, 'r') as file:
            products = json.load(file)       
  
        for product in products:
            emb = product['embedding']
            emb_binary = np.array(emb).tobytes()
            item = Product.objects.filter(title = product['title']).first()
            item.emb = emb_binary
            item.save()
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated item embeddings'))        
        