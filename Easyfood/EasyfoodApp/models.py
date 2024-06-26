from django.db import models
from django.contrib.auth.models import User
import numpy as np

def get_default_array():
  default_arr = np.random.rand(1536)  # Adjust this to your desired default array
  return default_arr.tobytes()

class Product(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    emb = models.BinaryField(default=get_default_array())
    image = models.ImageField(upload_to='../static/EasyFood')
    price = models.IntegerField(blank=True, null=True)
    sys_description = models.CharField(max_length=1000, default="Descripción en clave")

    def __str__(self):
        return self.title
