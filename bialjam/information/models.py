from django.db import models
from datetime import date

# === models for Information app ===

class Information(models.Model):
    """
    The Information class defines the information about BialJam contest. Each information has fields:

        1. name - full name of the contest
        2. address - exact address where the contest is taking place
        3. phone_number
        4. description - details about the contest
        5. email
        6. contest_date - date when the next edition will start
    """
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    email = models.EmailField(default='a@b.c')
    contest_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name

    @staticmethod
    def getDaysToContest():
        if Information.objects.count() != 0:
            info = Information.objects.last()
            return (info.contest_date - date.today()).days
        else:
            return 0
