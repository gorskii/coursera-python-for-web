from django.test import SimpleTestCase
from django.urls import reverse, resolve
from routing.views import simple_route


class TestSimpleRouteUrls(SimpleTestCase):
    """Test urls resolving simple_route path"""

    def test_simple_route_resolves(self):
        url = reverse('routing:simple_route')
        self.assertEqual(resolve(url).func, simple_route)
