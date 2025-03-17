from django import forms
from .models import Category,FooItem
from accounts.validators import allow_only_image_validators
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['category_name','description']


class FoodItemForm(forms.ModelForm):
    image=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info w-100'}))
    class Meta:
        model=FooItem
        fields=['category','food_title','description','price','image','is_available']
