from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth.password_validation import validate_password
from .models import Location
from .models import TestModel
from .models import Picture
from .models import Item
from .models import Memo
from .models import Trip

# User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Retype password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def clean(self):
        cleaned_date = super().clean()
        password = cleaned_date.get('password')
        confirm_password = cleaned_date.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('Your password does not match.')
        
    def save(self, commit=False):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        user.save()
        return user
    
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password','is_staff', 'is_active', 'is_superuser')

    def clean_password(self):
        return self.initial['password']
    
class RegistForm(forms.ModelForm):
    username = forms.CharField(label='Name')
    email = forms.EmailField(label='Mail Address')
    password = forms.CharField(label='Password', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='Retype password', widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('Your password does not match.')
    
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class LoginForm(forms.Form):
    email = forms.CharField(label='Mail Address')
    password = forms.CharField(label='Password',widget=forms.PasswordInput)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address']
        
class SingleUploadModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = '__all__'

class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        fields = ['image']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name']

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        fields = ['category', 'detail']

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'  # または、フォームに含めたいフィールドをリスト形式で指定