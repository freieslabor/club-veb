from django.forms import ModelForm, Textarea
from datetimewidget.widgets import DateWidget
from club_veb.models import Booking


class BookingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Booking
        exclude = []
        widgets = {
            'date': DateWidget(attrs={'id': "yourdatetimeid"}, usel10n=True, bootstrap_version=3),
            'headline': Textarea(attrs={'rows': 3}),
            'description': Textarea(attrs={'rows': 15}),
        }
