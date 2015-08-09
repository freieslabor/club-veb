from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .forms import BookingForm
from .models import Booking

from datetime import date, datetime, timedelta
from dateutil.parser import parse


def zentrale(request):
    return render(request, 'zentrale.html')


def programm(request):
    bookings = Booking.objects.all()
    return render(request, 'programm.html', {
                  'bookings': bookings,
                  })


def kontakt(request):
    return render(request, 'kontakt.html')


def galerie(request):
    return render(request, 'galerie.html')


def intern_uebersicht(request):
    return render(request, 'intern/uebersicht.html')


def intern_booking(request, year):
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

    return render(request, 'intern/booking.html', {
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

    booking = Booking.objects.get(id=id) if id else None

    if request.method == 'POST':
        bookingForm = BookingForm(request.POST, request.FILES)

        if bookingForm.is_valid():
            if booking:
                booking.__dict__.update(bookingForm.cleaned_data)
            else:
                booking = bookingForm
            booking.save()
            year = bookingForm.cleaned_data['date'].year
            return HttpResponseRedirect(
                reverse('club_veb.views.intern_booking', args=[year])
            )
    elif booking:
        bookingForm = BookingForm(instance=booking)
    else:
        bookingForm = BookingForm(initial={'date': date})

    return render(request, 'intern/booking_edit.html',
                  {'booking': bookingForm, 'id': id})


def intern_schichtplan(request):
    return render(request, 'intern/schichtplan.html')


def intern_todo(request):
    return render(request, 'intern/todo.html')


def intern_clubtreffen(request):
    return render(request, 'intern/clubtreffen.html')


def intern_benutzer(request):
    return render(request, 'intern/benutzer.html')


def intern_mail(request):
    return render(request, 'intern/mail.html')


def intern_kollektiv(request):
    return render(request, 'intern/kollektiv.html')
