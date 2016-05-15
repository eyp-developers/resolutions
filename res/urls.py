from django.conf.urls import url
from django.conf.urls.static import static

import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^download.pdf$', views.download, name='download'),
    url(r'^session/(?P<session_id>[0-9]+)/$', views.session, name='session'),
    url(r'^committee/(?P<committee_id>[0-9]+)/$', views.committee, name='committee'),
    url(r'^clause/(?P<clause_id>[0-9]+)/$', views.clause, name='clause'),
    url(r'^resolution-(?P<committee_id>[0-9]+).pdf$', views.resolution, name='resolution'),
]
