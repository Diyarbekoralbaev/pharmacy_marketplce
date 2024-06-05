from django.db import models


class Drug(models.Model):
    drug_name = models.CharField(max_length=100)
    description = models.TextField(blank=False,)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/drugs', default='images/drugs/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0)
    expiration_date = models.DateField(blank=False,)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=False,)
    manufacturer_country = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=100)
    active_substance = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    dozens = models.IntegerField(default=0, blank=False,)
    seller = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.drug_name
    
    class Meta:
        ordering = ['created_at']