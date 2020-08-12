from django.conf.urls import url
from routing.views import simple_route, slug_route

app_name = 'routing'

urlpatterns = [
    url(r'^simple_route/$', simple_route, name='simple_route'),
    url(r'^slug_route/([\da-z_-]{1,16})$', slug_route, name='slug_route'),
]
