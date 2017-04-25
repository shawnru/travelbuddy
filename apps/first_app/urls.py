from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.travels),
    url(r'^logout$', views.logout),
    url(r'^trip/(?P<id>\d+)$', views.trip),
    url(r'^addpage$', views.addpage),
    url(r'^join/(?P<id>\d+)$', views.join),
    url(r'^add$', views.add),
    # url(r'^session-test/$', views.session_test_1),
    # url(r'^session-test/done/$', views.session_test_2),

]
