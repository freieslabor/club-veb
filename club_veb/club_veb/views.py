from django.shortcuts import render
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
    else:
        booking = BookingForm()

    return render(request, 'planung.html', {'booking': booking})
