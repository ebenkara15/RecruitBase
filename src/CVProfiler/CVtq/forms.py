from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from .models import AppUser, Profile


class AppUserCreationForm(UserCreationForm):
    #Some trusted or accepted domains
    # __domains_accepted = ('example.com', 'gmail.com')

    class Meta:
        model = AppUser
        fields = ['username', 'email', 'password1', 'password2',]

    def clean_email(self):
        email_to_check = self.cleaned_data.get('email')

        # if not email_to_check.endswith(self.__domains_accepted):
        #     raise ValidationError(_("You can't register with this email - Enter your <domains> email address"))

        return email_to_check

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


