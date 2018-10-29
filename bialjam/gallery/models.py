from django.db import models


# === Models for Gallery app ===

def directory_path(instance, filename):
    return 'images/{0}/{1}'.format(instance.directory.name, filename)


class Directory(models.Model):
    """
    The Directory class defines the photos' directories. Each directory has fields:

        1. name
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Image(models.Model):
    """
    The Image class defines the photo in gallery. Each image has fields:

        1. directory - name of the directory the photo belongs to
        2. image - path to photo directory in project files
    """
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=directory_path, blank=True, null=True)


