from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
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
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Retype password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
    
    def clean(self):
        cleaned_date = super().clean()
        password = cleaned_date.get('password')
        confirm_password = cleaned_date.get('confirm_password')
        if password != confirm_password:
            raise ValidationError('パスワードが一致しません')
        
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
    username = forms.CharField(label='名前')
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='パスワード再入力', widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password != confirm_password:
            raise forms.ValidationError('パスワードが一致しません')
    
    def save(self, commit=False):
        user = super().save(commit=False)
        validate_password(self.cleaned_data['password'], user)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label='メールアドレス')
    password = forms.CharField(label='パスワード', widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  # requestをkwargsから取得し、インスタンス変数に保存
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        if email and password:
            # authenticateメソッドを呼び出す際にrequestオブジェクトを使用
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None or not self.user_cache.is_active:
                raise ValidationError("ログインが無効です。もう一度試してください")

        return cleaned_data

    def get_user(self):
        return self.user_cache

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['name', 'address']
        
class SingleUploadModelForm(forms.ModelForm):
    class Meta:
        model = TestModel
        fields = '__all__'

class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = '__all__'  # または、フォームに含めたいフィールドをリスト形式で指定
        exclude = ('user',)  # userフィールドを除外

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
        labels = {
            'category': 'カテゴリー',
            'detail': '詳細',
        }
    
    def __init__(self, *args, **kwargs):
        self.trip = kwargs.pop('trip', None)
        super(MemoForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        memo = super(MemoForm, self).save(commit=False)
        memo.trip = self.trip
        if commit:
            memo.save()
        return memo