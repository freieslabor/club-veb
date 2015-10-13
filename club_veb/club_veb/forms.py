from django import forms
from django.contrib.auth.forms import UserCreationForm
from datetimewidget.widgets import DateWidget, DateTimeWidget

from club_veb.models import Booking, Contact, ClubMeeting
from django.contrib.auth.models import User

from photologue.forms import UploadZipForm
from photologue.admin import GalleryAdminForm, PhotoAdminForm
from photologue.models import Gallery, Photo

from captcha.fields import CaptchaField


class UserFullnameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.get_full_name() == '':
            return obj.username
        else:
            return obj.get_full_name()


class BookingForm(forms.ModelForm):
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
    image = forms.ImageField(label=('Bild'), required=False,
                             widget=forms.FileInput,
                             error_messages={'invalid': ("Image files only")})

    date = forms.DateField(input_formats=["%d.%m.%Y"], required=True,
                           widget=DateWidget(usel10n=True,
                           attrs={'id': 'datetime'},
                           bootstrap_version=3))

    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Booking
        exclude = []
        widgets = {
            'description': forms.Textarea(attrs={'rows': 15}),
        }


class ContactForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = Contact
        exclude = []
        widgets = {
            'message': forms.Textarea(attrs={'rows': 8}),
        }


class ClubMeetingForm(forms.ModelForm):
    host = UserFullnameChoiceField(queryset=User.objects.all(),
                                   label='Gastgeber')

    date = forms.DateTimeField(input_formats=["%d.%m.%Y %H:%M:%S"], required=True,
                               widget=DateTimeWidget(usel10n=True,
                               attrs={'id': 'datetime_clubtreffen'},
                               bootstrap_version=3))

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


class VEBUploadZipForm(UploadZipForm):
    # hide useless fields for our usecase
    caption = forms.CharField(required=False, initial="",
                              widget=forms.HiddenInput())
    description = forms.CharField(required=False, initial="",
                                  widget=forms.HiddenInput())
    is_public = forms.CharField(required=False, initial=True,
                                widget=forms.HiddenInput())


class UserInfoForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1',
                  'password2')


class VEBGalleryAdminForm(GalleryAdminForm):
    class Meta:
        model = Gallery
        exclude = ['sites', 'is_public', 'slug']

        options = {
            'format': 'mm/dd/yyyy hh:ii',
            'autoclose': True,
            }
        widgets = {
            'date_added': DateTimeWidget(attrs={'id': 'datetime_galerie'},
                                         bootstrap_version=3, options=options),
        }


class VEBPhotoAdminForm(PhotoAdminForm):
    class Meta:
        model = Photo
        exclude = ['slug', 'caption', 'date_added', 'is_public', 'sites',
                   'crop_from', 'effect']
