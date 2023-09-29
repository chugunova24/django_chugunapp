from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *
from text_gen.forms import MyModelChoiceField


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', max_length=50, required=True)
    email = forms.EmailField(label='Email', required=True)
    password1 = forms.CharField(label='Пароль', required=True)
    password2 = forms.CharField(label='Повтор пароля', required=True)

    username.widget.attrs.update({'class': 'form-control'})
    email.widget.attrs.update({'class': 'form-control'})
    password1.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["image"].widget = forms.FileInput()
        self.fields["image"].label = "Image of profile"
        self.fields["first_name"].label = "Name"
        self.fields["last_name"].label = "Surname"

        self.queryset = self.get_queryset()

        self.fields["country"] = forms.ChoiceField(choices=self.queryset["countries"])
        # self.fields["country"] = MyModelChoiceField(queryset=self.queryset["countries"])
        self.fields["city"] = MyModelChoiceField(queryset=self.queryset["cities"])


        for field in self.Meta.fields:
            self.fields[field].required = False
            self.fields[field].widget.attrs.update({
                "class": "form-control h-100",
            })

        self.fields["first_name"].widget.attrs.update({
            "placeholder": "input your name",
        })
        self.fields["last_name"].widget.attrs.update({
            "placeholder": "input your surname",
        })

        self.fields["phone_number"].widget.attrs.update({
            "placeholder": "input your phone number",
        })

    def get_queryset(self):
        cities = CitiesOfCountry.objects.select_related("country").all()

        empty_label = [["", "---------"]]
        countries = empty_label + [[int(i.country_id), i.country.name] for i in list(cities)]
        countries = [i for n, i in enumerate(countries) if i not in countries[:n]]

        self.queryset = {}
        self.queryset["cities"] = cities
        self.queryset["countries"] = countries

        return self.queryset

    def clean_country(self):
        # country = self.cleaned_data.get("country",  False)
        country = self.cleaned_data.get("country")

        country = Country(id=country)
        return country

    class Meta:
        model = Profile
        fields = ['image', 'first_name', 'last_name', 'phone_number', 'country', 'city']