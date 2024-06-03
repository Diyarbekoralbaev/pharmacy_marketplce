from django.db import models

# Create your models here.

class Drug(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False,)
    description = models.TextField(null=False, blank=False,)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,)
    image = models.ImageField(upload_to='images/drugs', null=False, blank=False, default='images/drugs/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=False, blank=False,)


    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']