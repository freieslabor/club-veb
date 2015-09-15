from django.forms import ModelForm, Textarea, ModelChoiceField, ImageField, \
    FileInput
from datetimewidget.widgets import DateWidget, DateTimeWidget

from club_veb.models import Booking, Contact, ClubMeeting
from django.contrib.auth.models import User


class UserFullnameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.get_full_name() == '':
            return obj.username
        else:
            return obj.get_full_name()


class BookingForm(ModelForm):
    responsible = UserFullnameChoiceField(queryset=User.objects.all(),
                                          label='Verantwortlich',
                                          required=False)
    early_shift1 = UserFullnameChoiceField(queryset=User.objects.all(),
                                           label='Frühschicht #1',
                                           required=False)
    early_shift2 = UserFullnameChoiceField(queryset=User.objects.all(),
                                           label='Frühschicht #2',
                                           required=False)

    late_shift1 = UserFullnameChoiceField(queryset=User.objects.all(),
                                          label='Spätschicht #1',
                                          required=False)
    late_shift2 = UserFullnameChoiceField(queryset=User.objects.all(),
                                          label='Spätschicht #2',
                                          required=False)

    band_care1 = UserFullnameChoiceField(queryset=User.objects.all(),
                                         label='Bandbetreuung #1',
                                         required=False)
    band_care2 = UserFullnameChoiceField(queryset=User.objects.all(),
                                         label='Bandbetreuung #2',
                                         required=False)

    # use FileInput widget to avoid image url display
    image = ImageField(label=('Bild'), required=False, widget=FileInput,
                       error_messages={'invalid': ("Image files only")})

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Booking
        exclude = []
        options = {'format': 'mm/dd/yyyy'}
        widgets = {
            'date': DateWidget(attrs={'id': 'datetime'},
                               bootstrap_version=3, options=options),
            'headline': Textarea(attrs={'rows': 3}),
            'description': Textarea(attrs={'rows': 15}),
        }


class ContactForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Contact
        exclude = []
        widgets = {
            'message': Textarea(attrs={'rows': 8}),
        }


class ClubMeetingForm(ModelForm):
    host = UserFullnameChoiceField(queryset=User.objects.all(),
                                   label='Gastgeber')

    def __init__(self, *args, **kwargs):
        super(ClubMeetingForm, self).__init__(*args, **kwargs)
        # set host dropdown initially to current user
        if 'user' in kwargs:
            self.fields['host'].initial = kwargs['user']
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = ClubMeeting
        exclude = []
        options = {
            'format': 'mm/dd/yyyy hh:ii',
            'autoclose': True,
            }
        widgets = {
            'date': DateTimeWidget(attrs={'id': 'datetime_clubtreffen'},
                                   bootstrap_version=3, options=options),
        }
