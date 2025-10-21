from django.db import models
# from traitlets import default
# from authapp.models import User
class Categories(models.Model):
    name = models.CharField(max_length = 255, null= False )
    description = models.TextField()
    def __str__(self):
        return self.name

class Product(models.Model):
    Categories= models.ForeignKey(Categories, on_delete=models.CASCADE )
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)  # New field
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name






