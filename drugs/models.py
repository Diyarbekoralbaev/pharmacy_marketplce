from django.db import models


class Drug(models.Model):
    drug_name = models.CharField(max_length=100, null=False, blank=False,)
    description = models.TextField(null=False, blank=False,)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False,)
    image = models.ImageField(upload_to='images/drugs', null=False, blank=False, default='images/drugs/default.jpg')
    created_at = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=0, null=False, blank=False,)
    expiration_date = models.DateField(null=False, blank=False,)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=False, blank=False,)
    manufacturer_country = models.CharField(max_length=100, null=False, blank=False,)
    manufacturer = models.CharField(max_length=100, null=False, blank=False,)
    active_substance = models.CharField(max_length=100, null=False, blank=False,)
    type = models.CharField(max_length=100)
    dozens = models.IntegerField(default=0, null=False, blank=False,)

    def __str__(self):
        return self.drug_name
    
    class Meta:
        ordering = ['created_at']