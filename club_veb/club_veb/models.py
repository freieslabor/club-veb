from django.db import models
from django.contrib.auth.models import User

from .fields import STATE

import datetime


class Booking(models.Model):
    date = models.DateField(verbose_name='Termin')
    name = models.CharField(max_length=200, verbose_name='Name')
    headline = models.CharField(max_length=200, verbose_name='Überschrift')
    description = models.CharField(max_length=1000, verbose_name='Pressetext')
    type = models.CharField(max_length=50, verbose_name='Art')
    link = models.CharField(max_length=70, verbose_name='Link', blank=True)
    image = models.ImageField(verbose_name='Bild', upload_to='event_image',
                              blank=True)
    responsible = models.ForeignKey(User, verbose_name='Verantwortlich')
    state = models.IntegerField(verbose_name='Status', choices=STATE.items())

    def __str__(self):
        return self.name

    def simple_output(self):
        if self.responsible and self.responsible.get_full_name() == '':
            responsible = self.responsible.username
        else:
            responsible = self.responsible.get_full_name()

        return {
            'id': self.id,
            'date': self.date,
            'type': self.type,
            'name': self.name,
            'responsible': responsible,
            'state': STATE[self.state]
        }

    class Meta:
        app_label = 'club_veb'
        verbose_name = 'Booking'
