from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from string import ascii_lowercase, ascii_uppercase, digits, punctuation


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


class UpperCaseValidator:

    def validate(self, password, user=None):
        contains_upper = False
        for character in password:
            if character in ascii_uppercase:
                contains_upper = True
                break
        if not contains_upper:
            raise ValidationError(
                _("This password must contain at least one uppercase letter."),
                code="password_must_contain_uppercase_letter",
            )
        
    def get_help_text(self):
        return _("Your password must contain at least one uppercase letter.")


class DigitValidator:

    def validate(self, password, user=None):
        contains_digits = False
        for character in password:
            if character in digits:
                contains_digits = True
                break
        if not contains_digits:
            raise ValidationError(
                _("This password must contain at least one digit."),
                code="password_must_contain_digits",
            )
        
    def get_help_text(self):
        return _("Your password must contain at least one digit.")


class PunctuationValidator:

    def validate(self, password, user=None):
        contains_punctuation = False
        for character in password:
            if character in punctuation:
                contains_punctuation = True
                break
        if not contains_punctuation:
            raise ValidationError(
                _(f"This password must contain at least one punctuation {punctuation}."),
                code="password_must_contain_punctuation",
            )
        
    def get_help_text(self):
        return _(f"Your password must contain at least one punctuation {punctuation}.")