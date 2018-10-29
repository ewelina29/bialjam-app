# Create your views here.
from django.contrib import messages
from django.template import loader

from .models import Information
from bialjam.core import CustomHttpResponse
from django.utils.translation import ugettext_lazy as _

# === Views for Information app ===

"""
Information app includes the following views:

 1. **Information** - Return information about contest.  (jump to section in [[views.py#view_information]] )
 """


# === view_information ===
def view_information(request):
    """
    Return information about contest
    """
    try:
        info = Information.objects.last()
    except Information.DoesNotExist:
        messages.error(request, _('No information'))
        info = ""
    template = loader.get_template('information/information.html')
    context = {
        'info': info
    }
    return CustomHttpResponse.send(template, context, request)
