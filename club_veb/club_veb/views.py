from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from django.contrib import messages
from django.contrib.auth.models import User

from .forms import BookingForm, ContactForm, ClubMeetingForm, \
    VEBUploadZipForm
from .models import Booking, ClubMeeting, VEBGalleryAdminForm, \
    VEBPhotoAdminForm

from photologue import models as photo_models
from photologue import views as photo_views

from datetime import date, datetime, timedelta
from dateutil.parser import parse


def zentrale(request):
    bookings = Booking.objects.filter(date__gte=date.today()).order_by('date')
    return render(request, 'zentrale.html', {'bookings': bookings[:1]})


def programm(request):
    bookings = Booking.objects.filter(date__gte=date.today()).order_by('date')
    return render(request, 'programm.html', {'bookings': bookings[:5]})


def kontakt(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            send_mail(
                '[VEB] %s' % form.cleaned_data['subject'],
                form.cleaned_data['message'],
                form.cleaned_data['mail'],
                ['basti@freieslabor.org'],
                fail_silently=False
            )

            messages.success(request, 'Vielen Dank für die Nachricht!')
            form = ContactForm()
        else:
            messages.error(request, 'Formular unvollständig.')
    else:
        form = ContactForm()
        print(form)

    return render(request, 'kontakt.html', {'contact': form})


class VEBGalleryListView(photo_views.GalleryListView):
    paginate_by = 3


def intern_galerie(request):
    data = {
            'galleries': photo_models.Gallery.objects.all(),
            'photos': photo_models.Photo.objects.all(),
    }
    return render(request, 'intern/galerie.html', data)


def intern_galerie_edit(request, id):
    gallery = photo_models.Gallery.objects.get(pk=id) if id else None

    if request.method == 'POST':
        form = VEBGalleryAdminForm(request.POST, instance=gallery)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(
                reverse('club_veb.views.intern_galerie'))

    else:
        form = VEBGalleryAdminForm(instance=gallery)

    return render(request, 'intern/galerie_edit.html',
                  {'gallery': form, 'id': id})


def intern_galerie_del(request, id):
    gallery = get_object_or_404(photo_models.Gallery, pk=id)
    gallery.delete()
    return HttpResponseRedirect(reverse('club_veb.views.intern_galerie'))


def intern_galerie_photo_edit(request, id):
    photo = photo_models.Photo.objects.get(pk=id) if id else None

    if request.method == 'POST':
        form = VEBPhotoAdminForm(request.POST, request.FILES, instance=photo)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(
                reverse('club_veb.views.intern_galerie'))

    else:
        form = VEBPhotoAdminForm(instance=photo)

    return render(request, 'intern/galerie_edit.html',
                  {'gallery': form, 'id': id})


def intern_galerie_photo_del(request, id):
    photo = get_object_or_404(photo_models.Photo, pk=id)
    photo.delete()
    return HttpResponseRedirect(reverse('club_veb.views.intern_galerie'))


def intern_galerie_photo_zip_upload(request):
    if request.method == 'POST':
        form = VEBUploadZipForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect(
                reverse('club_veb.views.intern_galerie'))

    else:
        form = VEBUploadZipForm()

    return render(request, 'intern/galerie_edit.html', {'gallery': form})


def intern_uebersicht(request):
    return render(request, 'intern/uebersicht.html')


def intern_booking(request, year):
    return booking_table(request, year, 'intern/booking.html')


def booking_table(request, year, template):
    current_year = datetime.now().year
    if not year:
        year = current_year
    else:
        year = int(year)

    weekday = 2
    start = date(year, 1, 1)
    bookings = []

    # get all defined weekdays
    while start.year == year:
        bookings_on_date = Booking.objects.filter(date=start)
        for booking in bookings_on_date:
            bookings.append(booking.simple_output())

        # insert dummy event if no event on specific weekday yet
        if bookings_on_date.count() == 0 and start.weekday() == weekday:
            dummy = {
                'id': start.strftime('%Y-%m-%d'),
                'date': start,
                'type': '',
                'name': '',
                'responsible': '',
                'state': 'frei',
            }
            bookings.append(dummy)
        start += timedelta(days=1)

    # show year range
    if Booking.objects.count() == 0:
        first_year = current_year
    else:
        first_year = Booking.objects.order_by('date').first().date.year
    year_range = range(first_year, current_year+2)

    return render(request, template, {
                  'bookings': bookings,
                  'year': year,
                  'year_range': year_range,
                  })


def intern_booking_edit(request, id):
    # parse id or date
    try:
        id = int(id)
    except (ValueError, TypeError):
        try:
            date = parse(id)
        except (TypeError, AttributeError):
            date = ''

        id = None

    booking = Booking.objects.get(pk=id) if id else None

    if request.method == 'POST':
        form = BookingForm(request.POST, request.FILES, instance=booking)

        if form.is_valid():
            form.save()
            year = form.cleaned_data['date'].year
            return HttpResponseRedirect(
                reverse('club_veb.views.intern_booking', args=[year])
            )
    elif booking:
        form = BookingForm(instance=booking)
    else:
        form = BookingForm(initial={'date': date})

    return render(request, 'intern/booking_edit.html',
                  {'booking': form, 'id': id})


def intern_schichtplan(request, year):
    return booking_table(request, year, 'intern/schichtplan.html')


def intern_todo(request):
    return render(request, 'intern/todo.html')


def intern_clubtreffen(request, year):
    current_year = datetime.now().year
    if not year:
        year = current_year
    else:
        year = int(year)

    meetings = ClubMeeting.objects.filter(date__year=year)

    # show year range
    try:
        first_year = ClubMeeting.objects.order_by('date').first().date.year
    except AttributeError:
        first_year = current_year

    year_range = range(first_year, current_year+2)

    return render(request, 'intern/clubtreffen.html', {
                  'meetings': meetings,
                  'year': year,
                  'year_range': year_range,
                  })


def intern_clubtreffen_edit(request, id):
    clubMeeting = ClubMeeting.objects.get(pk=id) if id else None

    if request.method == 'POST':
        form = ClubMeetingForm(request.POST, instance=clubMeeting)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('club_veb.views.intern_clubtreffen')
            )
    else:
        form = ClubMeetingForm(instance=clubMeeting)

    return render(request, 'intern/clubtreffen_edit.html',
                  {'clubMeeting': form, 'id': id})


def intern_clubtreffen_del(request, id):
    meeting = get_object_or_404(ClubMeeting, pk=id)
    meeting.delete()
    return HttpResponseRedirect(reverse('club_veb.views.intern_clubtreffen'))


def intern_benutzer(request):
    return render(request, 'intern/benutzer.html')


def intern_mail(request):
    return render(request, 'intern/mail.html')


def intern_kollektiv(request):
    users = [user.first_name or user.username for user in User.objects.all()]
    return render(request, 'intern/kollektiv.html', {'users': users})
