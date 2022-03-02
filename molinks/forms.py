from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}), label='Login', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', max_length=100)
