from django import forms
from django_password_eye.fields import PasswordEye
from .models import Book,Category,Author,Member


class categoryform(forms.ModelForm):

    class Meta():
        model=Category
        fields=['name']


class authorform(forms.ModelForm):

    class Meta():
        model=Author
        fields=['author','about']


class bookform(forms.ModelForm):
   
    class Meta():
        model=Book
        fields=['title','date_pub','publisher','description','image','categ','author','page_num','file']


class memberform(forms.ModelForm):

    # Confirmpassword=forms.PasswordInput()  

    class Meta():
        model=Member
        fields=['name','email','password','about','image']

        widgets = {
            'password': forms.PasswordInput()
        }


class loginform(forms.Form):
     username=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
     password=PasswordEye()
     
    #  widegets={
    #      ' username': forms.TextInput( attrs={'classw':'form-control w-100'})
    #  }
    
     
class loginmember(forms.Form):
     membername=forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ''}))
     password=PasswordEye()




#    class Meta:
#       model=product
#       fields=['',',','']

    # name=forms.CharField(max_length=1100)
    # categ=forms.CharField(max_length=20)
    # quantity=forms.IntegerField()
    # price=forms.FloatField()
    # brand=forms.CharField(max_length=100)
    # color_pro=forms.CharField(max_length=20)
    # size_pro=forms.CharField(max_length=5)
    # image=forms.ImageField()
