from dataclasses import field
from django.forms import ModelForm, Textarea
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class CreateCustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ["user", "name", "phone", "email"]

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ["user"]

        # widgets = {
        #     'name': Textarea(attrs={'cols': 20, 'rows': 1}),
        # }
        # labels = {
        #     'name': _('Name'),
        # }
        # error_messages = {
        #     'name': {
        #         'max_length': _("This writer's name is too long."),
        #     },
        # }
        
