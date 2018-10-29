from django.contrib import messages
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Directory, Image
from bialjam.core import CustomHttpResponse
from django.utils.translation import ugettext_lazy as _

# === Views for Gallery app ===

"""
Gallery app includes the following views:


 1. **List of directiories** - List of all directories. Photos are segregated in directories for example -Bialjam2016. (jump to section in [[views.py#list_directories]] )
 2. **List of photos** - List of all photos in chosen directory( jump to section in [[views.py#list_photos]] )
 """


# === list_directories ===
def list_directories(request):
    """
    List of all directories. Photos are segregated in directories,  e.g.: Bialjam2016.
    """
    template = loader.get_template('gallery/directories_list.html')

    directory_list = Directory.objects.all()
    paginator = Paginator(directory_list, 6)  # Show 6 directories per page

    if len(directory_list) == 0:
        messages.error(request, _('No photos to show'))
    else:
        page = request.GET.get('page')
        try:
            directories = paginator.page(page)
        except PageNotAnInteger:
            directories = paginator.page(1)
        except EmptyPage:
            directories = paginator.page(paginator.num_pages)

        context = {
            'directories': directories
        }

        return CustomHttpResponse.send(template, context, request)
    return CustomHttpResponse.send(template, {}, request)


# === list_photos ===
def list_photos(request, id):
    """
    List of all photos in chosen directory
    """
    template = loader.get_template('gallery/photos_list.html')

    directory = Directory.objects.get(id=id)

    photo_list = Image.objects.filter(directory=directory)
    paginator = Paginator(photo_list, 6)  # Show 6 photos per page

    page = request.GET.get('page')
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        photos = paginator.page(1)
    except EmptyPage:
        photos = paginator.page(paginator.num_pages)

    context = {
        'photos': photos
    }

    return CustomHttpResponse.send(template, context, request)
