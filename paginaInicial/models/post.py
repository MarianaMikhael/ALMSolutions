import re

from django.db import models
from datetime import datetime
from django.core import validators

from django.utils.translation import ugettext_lazy as _


#defaultAPI = datetime.now().isoformat() + 'Z'
#default=datetime.now
class Post(models.Model):
    summary = models.CharField("Title", max_length=500, null=True)
    location = models.CharField("Title", max_length=500, null=True)
    description = models.CharField("Title", max_length=500, null=True)
    start = models.DateTimeField("Start date", default=datetime.now, null=True)  # start event date
    end = models.DateTimeField("End date", default=datetime.now, null=True)  # end event date default=datetime.now, 
    event_id = models.CharField("Event id", max_length=1024, null=True, default='N/A')  # event id from google calendar
    email = models.EmailField(_('email address'), max_length=255, validators=[
        validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid e-mail'),
        _('invalid'))], null=False, blank=False)

    def __str__(self):
        return self.summary
