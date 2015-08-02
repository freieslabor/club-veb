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


def impressum(request):
    return render(request, 'impressum.html')


def planung(request):
    if request.method == "POST":
        booking = BookingForm(request.POST, request.FILES)
        if booking.is_valid():
            booking.save()
            return HttpResponseRedirect(
                reverse("club_veb.views.zentrale")
            )
    else:
        booking = BookingForm()

    return render(request, 'planung.html', {'booking': booking})
