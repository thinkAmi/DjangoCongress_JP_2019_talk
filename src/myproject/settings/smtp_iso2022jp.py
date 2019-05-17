from .my_smtp import *

# EMAIL_BACKENDを差し替え
EMAIL_BACKEND = 'myapp.email_backends.Iso2022JpEmailBackend'
