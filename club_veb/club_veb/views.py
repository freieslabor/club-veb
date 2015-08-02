from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from club_veb.forms import BookingForm


def zentrale(request):
    return render(request, 'zentrale.html')


def programm(request):
    return render(request, 'programm.html')


def kontakt(request):
    return render(request, 'kontakt.html')


def galerie(request):
    return render(request, 'galerie.html')


def intern_uebersicht(request):
    return render(request, 'intern/uebersicht.html')


def intern_booking(request):
    if request.method == 'POST':
        booking = BookingForm(request.POST, request.FILES)
        if booking.is_valid():
            booking.save()
            return HttpResponseRedirect(
                reverse('club_veb.views.zentrale')
            )
    else:
        booking = BookingForm()

    return render(request, 'intern/booking.html', {'booking': booking})


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
