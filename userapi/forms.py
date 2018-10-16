from django import forms

from userapi.models import User


class RegisterLoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ChangeNameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["name"]


class ChangeWalletForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "wallet"]


class ChangePhoneForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]


class ChangeGenderForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["gender"]


class ChangeAvaterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["avater"]


