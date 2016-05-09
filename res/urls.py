from django.conf.urls import url
from django.conf.urls.static import static

import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^session/(?P<session_id>[0-9]+)/$', views.session, name='session'),
    url(r'^session/(?P<session_id>[0-9]+)/committee/(?P<committee_id>[0-9]+)/$', views.committee, name='committee')
]
