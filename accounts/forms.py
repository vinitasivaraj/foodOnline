from django import forms
from .models import User,UserProfile
from .validators import allow_only_image_validators

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    confirm_Password=forms.CharField(widget=forms.PasswordInput())

    class Meta:

        model = User
        fields= ['first_name', 'last_name' ,'username','email','password']

    def clean(self):
            cleaned_date=super(UserForm,self).clean()
            password=cleaned_date.get('password')
            confirm_Password=cleaned_date.get('confirm_Password')

            if password != confirm_Password:
                 raise forms.ValidationError("Password does not match ")


class UserProfileForm(forms.ModelForm):
     profile_picture=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image_validators])
     cover_photo=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image_validators])
     address=forms.CharField(widget=forms.TimeInput(attrs={'placeholder':'Start Typing','required':'required'}))
    #  latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #  longitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
     class Meta:
          
         model =  UserProfile
         fields = ['profile_picture','cover_photo','address','country','state','city','pin_code','latitude','longitude']

     def __init__(self,*args,**kwargs):
          super(UserProfileForm,self).__init__(*args,**kwargs)
          for field in self.fields:
               if field=='latitude' or field=='longitude':
                    self.fields[field].widget.attrs['readonly']='readonly'
                    