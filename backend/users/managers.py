from multiprocessing.sharedctypes import Value
from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except Exception as e:
            raise ValidationError(_("You must provide a valid email address"))

    def create_user(self, email, password=None, **kwargs):
        if not 'username' in kwargs or not kwargs['username']:
            raise ValueError(_('Users must submit an username'))

        if not 'first_name' in kwargs or not kwargs['first_name']:
            raise ValueError(_('Users must submit a first name'))

        if not 'last_name' in kwargs or not kwargs['last_name']:
            raise ValueError(_('Users must submit a last name'))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_('Base User Account: An email address is required'))

        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user
