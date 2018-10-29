from django.template import loader

from .models import Vip, Lesson
from django.utils.translation import ugettext_lazy as _

from bialjam.core import CustomHttpResponse

# === Views for the Vip app ===

"""
 Vip app includes the follwing views:

 1. **Vip jury** - List of vips(jury, lectures or both) (jump to section in [[views.py#vip_jury]] )
 1. **Vip details** - Vip details (jump to section in [[views.py#vip_details]] )
 """


# === vip_jury ===
def vip_jury(request):
    """
    List of vips. It's possible to choose: jury, lectures or both.
    """
    template = loader.get_template('vip/vip.html')
    vip_list = Vip.objects.filter(guest_as__in=['JU', 'LE', 'BO']).order_by('name')
    context = {'vip_list': vip_list, 'title': _("Jury:")}
    return CustomHttpResponse.send(template, context, request)


# === vip_details ===
def vip_details(request, id):
    """
    Vip details with information about lessons
    """
    template = loader.get_template('vip/vip_details.html')

    try:
        vip = Vip.objects.get(id=id)

        lessons = Lesson.objects.filter(lecturer_id=id)

        context = {
            'vip': vip,
            'lessons': lessons
        }

    except Vip.DoesNotExist:
        context = None

    return CustomHttpResponse.send(template, context, request)
