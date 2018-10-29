from django.http import HttpResponse
from information.models import Information


class CustomHttpResponse:
    @staticmethod
    def send(template, context, request):
        info = Information.objects.last()
        if context is None:
            context={}
        if info is not None:
            context['days'] = Information.getDaysToContest()

        return HttpResponse(template.render(context, request))
