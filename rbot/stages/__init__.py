from __future__ import unicode_literals
from . import welcome

RBOT_STAGES = {'welcome': 'Welcome',
               'postal_code': 'PostalCode',
               'postal_code_failed': 'PostalCodeFailed'}
RBOT_STARTING_STAGE = welcome.Welcome

