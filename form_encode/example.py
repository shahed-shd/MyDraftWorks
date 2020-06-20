import re

from formencode import validators, Invalid

class SecurePassword(validators.FancyValidator):
    min = 3
    non_letter = 1
    letter_regex = re.compile(r'[a-zA-Z]')

    messages = {
        'too_few': 'Your password must be longer than %(min)i characters in your password',
        'non_letter': 'You must include at least %(non_letter)i characters in your password'
    }

    def _conver_to_python(self, value, state):
        return value.strip()


    def _validate_python(self, value, state):
        if len(value) < self.min:
            raise Invalid(self.message("too_few", state, min=self.min), value, state)

        non_letters = self.letter_regex.sub('', value)

        if len(non_letters) < self.non_letter:
            raise Invalid(self.message("non_letter", state, non_letter=self.non_letter), value, state)
