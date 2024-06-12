# Autor:Jovan Babovic
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Nalog
from django.contrib.auth import authenticate


class RegistrationForm(UserCreationForm):
    """
    A form for registering new users. It includes fields for email, username, and password.
    """

    email = forms.EmailField(max_length=255, help_text='Potrebno! Dodajte validnu email adresu!')

    class Meta:
        model = Nalog
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        """
        Validates the email address to ensure it's unique.
        """
        email = self.cleaned_data['email'].lower()
        if Nalog.objects.filter(email=email).exists():
            raise forms.ValidationError("Email već postoji!")
        return email

    def clean_username(self):
        """
        Validates the username to ensure it's unique.
        """
        username = self.cleaned_data['username'].lower()
        if Nalog.objects.filter(username=username).exists():
            raise forms.ValidationError("Korisničko ime već postoji!")
        return username

    def clean_password2(self):
        """
        Validates that the two password entries match and meet certain criteria.
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Lozinke se ne poklapaju!")

        if len(password1) < 8:
            raise forms.ValidationError("Lozinka mora sadržati najmanje 8 karaktera!")

        return password2


class LoginForm(AuthenticationForm):
    """
    A form for logging in existing users. It includes fields for username and password.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    username = forms.CharField(label="username", max_length=255)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    
    class Meta:
        fields = ['username', 'password'] 

    def clean(self):
        """
        Validates the login credentials.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                self.add_error(None, "Korisničko ime ili šifra je pogrešno.")
        return cleaned_data