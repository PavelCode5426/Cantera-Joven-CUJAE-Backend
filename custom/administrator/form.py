
from django.contrib.admin.forms import AdminAuthenticationForm
from django.forms.fields import TextInput
from django.contrib.auth.forms import AuthenticationForm, UsernameField


class CustomAdminLoginForm(AdminAuthenticationForm):
    username = UsernameField(widget=TextInput(attrs={"autofocus": True}))