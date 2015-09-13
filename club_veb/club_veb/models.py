from django.db import models
from django.contrib.auth.models import User

from .fields import STATE, SUBJECTS


class Booking(models.Model):
    date = models.DateField(verbose_name='Termin')
    name = models.CharField(max_length=200, verbose_name='Name')
    headline = models.CharField(max_length=200, verbose_name='Überschrift')
    description = models.CharField(max_length=1000, verbose_name='Pressetext')
    type = models.CharField(max_length=50, verbose_name='Art')
    link = models.CharField(max_length=70, verbose_name='Link', blank=True)
    image = models.ImageField(verbose_name='Bild', upload_to='event_image',
                              blank=True)
    responsible = models.ForeignKey(User, verbose_name='Verantwortlich',
                                    blank=True, null=True)
    state = models.IntegerField(verbose_name='Status', choices=STATE.items())

    early_shift1 = models.ForeignKey(User, verbose_name='Frühschicht #1',
                                     related_name='+', blank=True, null=True)
    early_shift2 = models.ForeignKey(User, verbose_name='Frühschicht #2',
                                     related_name='+', blank=True, null=True)

    late_shift1 = models.ForeignKey(User, verbose_name='Spätschicht #1',
                                    related_name='+', blank=True, null=True)
    late_shift2 = models.ForeignKey(User, verbose_name='Spätschicht #2',
                                    related_name='+', blank=True, null=True)

    band_care1 = models.ForeignKey(User, verbose_name='Bandbetreuung #1',
                                   related_name='+', blank=True, null=True)
    band_care2 = models.ForeignKey(User, verbose_name='Bandbetreuung #2',
                                   related_name='+', blank=True, null=True)

    def __str__(self):
        return self.name

    def username(self, user):
        if not user:
            return None
        if user.get_full_name() == '':
            return user.username
        else:
            return user.get_full_name()

    def join_usernames(self, *users):
        return ' & '.join([self.username(user) for user in users if user])

    def simple_output(self):
        early_users = self.join_usernames(self.early_shift1, self.early_shift2)
        late_users = self.join_usernames(self.late_shift1, self.late_shift2)
        band_users = self.join_usernames(self.band_care1, self.band_care2)

        return {
            'id': self.id,
            'date': self.date,
            'type': self.type,
            'name': self.name,
            'responsible': self.username(self.responsible),
            'state': STATE[self.state],
            'early_shift': early_users,
            'late_shift': late_users,
            'band_care': band_users
        }

    class Meta:
        app_label = 'club_veb'
        verbose_name = 'Booking'


class Contact(models.Model):
    name = models.CharField(max_length=200, verbose_name='Ihr Name')
    mail = models.EmailField(max_length=100, verbose_name='E-Mail-Adresse')
    subject = models.CharField(max_length=200, verbose_name='Betreff',
                               choices=SUBJECTS.items())
    message = models.CharField(max_length=10000, verbose_name='Ihre Nachricht')
