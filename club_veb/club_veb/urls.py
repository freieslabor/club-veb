from django.conf.urls import include, url
from django.views.generic.base import TemplateView, RedirectView
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

from .views import VEBGalleryListView

urlpatterns = [
    url(r'^intern/login/$', auth_views.login),
    url(r'^intern/logout/$', auth_views.logout_then_login),

    url(r'^intern/password/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),

    url(r'^intern/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^intern/password/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^intern/password/reset/$',
        auth_views.password_reset,
        name='password_reset'),

    url(r'^captcha/', include('captcha.urls')),

    url(r'^galerie/$(?P<id>\S+)?$', VEBGalleryListView.as_view(),
        name='galerie'),

    url(r'^programm/$', 'club_veb.views.programm', name='programm'),

    url(r'^kontakt/$', 'club_veb.views.kontakt', name='kontakt'),

    url(r'^intern/galerie/$', 'club_veb.views.intern_galerie',
        name='intern_galerie'),
    url(r'^intern/galerie/edit/(?P<id>\S+)?$',
        'club_veb.views.intern_galerie_edit', name='intern_galerie_edit'),
    url(r'^intern/galerie/del/(?P<id>\S+)?$',
        'club_veb.views.intern_galerie_del', name='intern_galerie_del'),
    url(r'^intern/galerie/photo/edit/(?P<id>\S+)?$',
        'club_veb.views.intern_galerie_photo_edit',
        name='intern_galerie_photo_edit'),
    url(r'^intern/galerie/photo/del/(?P<id>\S+)?$',
        'club_veb.views.intern_galerie_photo_del',
        name='intern_galerie_photo_del'),
    url(r'^intern/galerie/photo/upload/$',
        'club_veb.views.intern_galerie_photo_zip_upload',
        name='intern_galerie_photo_zip_upload'),

    url(r'^impressum/$', TemplateView.as_view(template_name='impressum.html'),
        name='impressum'),

    url(r'^intern/$',
        RedirectView.as_view(
            url='booking',
            permanent=False),
        name='intern_uebersicht'),

    url(r'^intern/booking/edit/(?P<id>\S+)?$',
        'club_veb.views.intern_booking_edit', name='intern_booking_edit'),
    url(r'^intern/booking/(?P<year>\S+)?$', 'club_veb.views.intern_booking',
        name='intern_booking'),

    url(r'^intern/schichtplan/(?P<year>\S+)?$',
        'club_veb.views.intern_schichtplan',
        name='intern_schichtplan'),

    url(r'^intern/todo$', 'club_veb.views.intern_todo', name='intern_todo'),

    url(r'^intern/clubtreffen/edit/(?P<id>\S+)?$',
        'club_veb.views.intern_clubtreffen_edit',
        name='intern_clubtreffen_edit'),
    url(r'^intern/clubtreffen/del/(?P<id>\S+)?$',
        'club_veb.views.intern_clubtreffen_del',
        name='intern_clubtreffen_del'),
    url(r'^intern/clubtreffen/(?P<year>\S+)?$',
        'club_veb.views.intern_clubtreffen',
        name='intern_clubtreffen'),

    url(r'^intern/benutzer/$', 'club_veb.views.intern_benutzer',
        name='intern_benutzer'),

    url(r'^intern/mail/$', 'club_veb.views.intern_mail', name='intern_mail'),

    url(r'^intern/kollektiv/$', 'club_veb.views.intern_kollektiv',
        name='intern_kollektiv'),

    url(r'^$', 'club_veb.views.zentrale', name='zentrale'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # devel only
