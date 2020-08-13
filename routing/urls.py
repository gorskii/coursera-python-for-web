from django.conf.urls import url

from routing.views import simple_route, slug_route, sum_route, sum_get_method

app_name = 'routing'

urlpatterns = [
    url(r'^simple_route/$', simple_route, name='simple_route'),
    url(r'^slug_route/([\da-z_-]{1,16})$', slug_route, name='slug_route'),
    url(r'^sum_route/(?P<first>-?\d+)/(?P<second>-?\d+)/$',
        sum_route, name='sum_route'),
    url(r'^sum_get_method/', sum_get_method, name='sum_get_method'),
]
