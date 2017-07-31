from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms
from .models import SwapContract, User, SwapDetails
from functools import partial
DateInput = partial(forms.DateInput, {'class': 'datepicker'})


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user


class NewPassword(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
        return user


class UserRegister(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserLogin(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password']


class AddSwap(forms.ModelForm):

    class Meta:
        model = SwapContract
        fields = ['swap_name', 'swap_type', 'margin_money']


class AddSwapContract(forms.ModelForm):
    swap_start_date = forms.DateField(widget=DateInput())
    swap_end_date = forms.DateField(widget=DateInput())

    class Meta:
        model = SwapDetails
        fields = ['swap_name', 'swap_sector', 'swap_margin', 'swap_base_curr', 'swap_start_date', 'swap_end_date']