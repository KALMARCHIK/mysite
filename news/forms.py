from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import formset_factory

from .models import *
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError


class ChangeUserInfoForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='Адрес электронной почты')

    class Meta:
        model = AdvUser
        fields = ('email', 'username', 'first_name', 'last_name')


class ChangePasswordForm(forms.ModelForm):
    password_new = forms.CharField(label='Новый пароль', widget=forms.PasswordInput)
    password_new2 = forms.CharField(label='Новый пароль (ещё раз)', widget=forms.PasswordInput)

    class Meta:
        model = AdvUser
        fields = ('password', 'password_new', 'password_new2')


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'rubric')
        widgets = {'user': forms.HiddenInput}


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": "form-control form-control-user", "placeholder": "Password"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Repeat Password",
            }
        )
    )
    def clean(self):
        cleaned_data = super(RegisterUserForm,self).clean()
        email = cleaned_data['email']
        username = cleaned_data['username']
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        errors = {}
        if AdvUser.objects.filter(email=email).exists():
            errors['email'] = ValidationError('Email уже занят')
        if AdvUser.objects.filter(username=username).exists():
            errors['username'] = ValidationError('Username уже занят')
        if password1 != password2:
            errors['password1'] = ValidationError('Пароли не совпадают')
        if errors:
            raise ValidationError(errors)
    class Meta:
        model = AdvUser
        fields = (
            "email",
            "username",
            'first_name',
            'last_name',
            'password1',
            'password2',
        )

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user",
                    "placeholder": "Username",
                }
            ),
            "email": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user",
                    "placeholder": "Email Address  *Optional",
                }
            ),
            "first_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user",
                    "placeholder": "Your Name",
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user",
                    "placeholder": "Last name",
                }
            ),
            "password1": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user",
                    "placeholder": "Password",
                }
            ),
            "password2": forms.TextInput(
                attrs={
                    "class": "form-control form-control-user",
                    "placeholder": "Repeat password",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    """Форма отзывов"""

    class Meta:
        model = Comment
        fields = ('content',)
        widget = {'author': forms.HiddenInput}


class ProstoForm(forms.Form):
    title = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Username",
    }))
    text = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control form-control-user",
        "placeholder": "Username",
    }))


ProstoFormSet = formset_factory(ProstoForm, extra=2)


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ('rating',)


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ('like',)


class RubricForm(forms.ModelForm):
    class Meta:
        model = Rubric
        fields = '__all__'
