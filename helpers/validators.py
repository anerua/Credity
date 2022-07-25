from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from string import ascii_lowercase


class LowerCaseValidator:

    def validate(self, password, user=None):
        contains_lower = False
        for character in password:
            if character in ascii_lowercase:
                contains_lower = True
                break
        if not contains_lower:
            raise ValidationError(
                _("This password must contain at least one lowercase letter."),
                code="password_must_contain_lowercase_letter",
            )
    
    def get_help_text(self):
        return _("Your password must contain at least one lowercase letter.")
