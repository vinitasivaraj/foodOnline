from django.db import models
from accounts.models import User
from menu.models import FooItem


# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    fooditem=models.ForeignKey(FooItem,on_delete=models.CharField)
    quantity=models.PositiveBigIntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.user
    

class Tax(models.Model):
    tax_type=models.CharField(max_length=20,unique=True)
    tax_percentage=models.DecimalField(decimal_places=2,max_digits=4,verbose_name='Tax Percentage (%)')
    is_active=models.BooleanField(default=True)


    class Meta:
        verbose_name_plural='Tax'
    def __str__(self):
        return self.tax_type
