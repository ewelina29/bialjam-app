from django.db import models
from django.core.exceptions import ValidationError

# === models for Vip app ===


JURY = 'JU'
LECTURER = 'LE'
BOTH = 'BO'


def directory_path(instance, filename):
    return 'images/vips/{0}'.format(filename)


class Vip(models.Model):
    """
    The Vip class defines the special guests (jury or lecturers). Each vip has fields:

        1. name - VIP's name
        2. surname - VIP's surname
        3. bio - short VIP's biography
        4. guest_as - VIP's role (one of the: Jury, Lecturer, Jury-Lecturer)
        5. image_path - path to the VIP's avatar
    """
    GUEST_CHOICES = (
        (JURY, 'Jury'),
        (LECTURER, 'Lecturer'),
        (BOTH, 'Jury-Lecturer')
    )
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=50)
    bio = models.CharField(max_length=300)
    guest_as = models.CharField(choices=GUEST_CHOICES, default=JURY, max_length=2)
    image_path = models.ImageField(upload_to=directory_path, blank=True, null=True)

    def __str__(self):
        return self.name + ' ' + self.surname


class Lesson(models.Model):
    """
    The Lesson class defines the lecture details. Each lesson has fields:

        1. date - exact date and time when the lecture will be taken
        2. subject - topic of the lecture
        3. lecturer - VIP (Lecturer) who will be conducting the lecture
    """
    date = models.DateTimeField()
    subject = models.CharField(max_length=100)
    lecturer = models.ForeignKey(Vip, on_delete=models.CASCADE, limit_choices_to={'guest_as__in': [LECTURER, BOTH]})

    def clean(self):

        if self.lecturer.guest_as == JURY:
            raise ValidationError('Chosen person is only in jury')
