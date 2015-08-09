from django.forms import ModelForm, Textarea, ModelChoiceField, ImageField, \
    FileInput
from datetimewidget.widgets import DateWidget

from club_veb.models import Booking
from django.contrib.auth.models import User


class UserFullnameChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.get_full_name() == '':
            return obj.username
        else:
            return obj.get_full_name()


class BookingForm(ModelForm):
    responsible = UserFullnameChoiceField(queryset=User.objects.all(),
                                          label='Verantwortlich')

    # use FileInput widget to avoid image url display
    image = ImageField(label=('Bild'), required=False, widget=FileInput,
                       error_messages = {'invalid': ("Image files only")})

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
