from django import forms
import models


class UserForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': 'Enter your username'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                          'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'type': 'password',
                                                             'placeholder': 'Enter your password'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    gender = forms.Select()
    sexual_orientation = forms.Select()

    LOOKING_FOR_CATEGORY = [('friend', 'Friends'), ('sex', 'Casual sex'), ('short', 'Short term relationship'), ('long', 'Long term relationship')]
    looking_for = forms.MultipleChoiceField(LOOKING_FOR_CATEGORY)

    class Meta:
        model = models.Dater
        fields = ['username', 'email', 'password', 'description', 'gender', 'sexual_orientation', 'looking_for']