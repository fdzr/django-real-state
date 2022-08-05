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

    def create_user(self, username, first_name, last_name, email, password=None, **kwargs):
        if not 'username':
            raise ValueError(_('Users must submit an username'))

        if not 'first_name':
            raise ValueError(_('Users must submit a first name'))

        if not 'last_name':
            raise ValueError(_('Users must submit a last name'))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_('Base User Account: An email address is required'))

        user = self.model(email=email,
                          first_name=first_name,
                          last_name=last_name,
                          username=username,
                          **kwargs)
        user.set_password(password)
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_active", False)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_active", True)
        kwargs.setdefault("is_superuser", True)

        if kwargs.get("is_staff") is False:
            raise ValueError(_("Superusers must have is_staff=True"))

        if kwargs.get("is_superuser") is False:
            raise ValueError(_("Superusers must have is_superuser=True"))

        if not password:
            raise ValueError(_("Superusers must have a password"))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError(_("Admin Account: An email address is required"))

        user = self.create_user(username,
                                first_name,
                                last_name,
                                email,
                                password,
                                **kwargs)
        user.save(using=self._db)
        return user
