from django.conf.urls import url
from routing.views import simple_route

app_name = 'routing'

urlpatterns = [
    url(r'^simple_route/$', simple_route, name='simple_route')
]
