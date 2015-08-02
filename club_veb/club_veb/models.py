from django.db import models
from django.contrib.auth.models import User


class Booking(models.Model):
    date = models.DateField(verbose_name='Termin')
    name = models.CharField(max_length=200, verbose_name='Name')
    headline = models.CharField(max_length=200, verbose_name='Überschrift')
    description = models.CharField(max_length=1000, verbose_name='Pressetext')
    type = models.CharField(max_length=50, verbose_name='Art')
    link = models.CharField(max_length=70, verbose_name='Link')
    image = models.ImageField(verbose_name='Bild')
    responsible = models.ForeignKey(User, verbose_name='Verantwortlich')
    state = models.IntegerField(verbose_name='Status', choices=(
        (1, 'geblockt'),
        (2, 'gebucht'),
        (3, 'frei'),
    ))

    def __str__(self):
        return self.name

    class Meta:
        app_label = 'club_veb'
        verbose_name = 'Booking'
