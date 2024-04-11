from django.core.management.base import BaseCommand
from EasyfoodApp.models import Product
class Command(BaseCommand):
    help = 'Vacía la base de datos eliminando todos los registros'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()
