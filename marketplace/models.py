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
