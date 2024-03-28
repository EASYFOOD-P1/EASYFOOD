from django.db import models

class Product(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='../static/EasyFood')
    price = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.title
