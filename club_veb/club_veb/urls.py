from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'club_veb.views.zentrale', name='zentrale'),
    url(r'^programm$', 'club_veb.views.programm', name='programm'),
    url(r'^kontakt$', 'club_veb.views.kontakt', name='kontakt'),
    url(r'^galerie$', 'club_veb.views.galerie', name='galerie'),
    url(r'^impressum$', 'club_veb.views.impressum', name='impressum'),
    url(r'^planung$', 'club_veb.views.planung', name='planung'),
    url(r'^admin/', include(admin.site.urls)),
]
