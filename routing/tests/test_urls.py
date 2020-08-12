from django.test import SimpleTestCase
from django.urls import reverse, resolve, NoReverseMatch
from routing.views import simple_route, slug_route


class TestSimpleRouteUrls(SimpleTestCase):
    """Test urls resolving simple_route path"""

    def test_simple_route_resolves(self):
        url = reverse('routing:simple_route')
        self.assertEqual(resolve(url).func, simple_route)


class TestSlugRouteUrls(SimpleTestCase):
    """Test urls resolving slug_route path"""

    def test_slug_route_resolves(self):
        url = reverse('routing:slug_route', args=['1-valid_slug'])
        self.assertEqual(resolve(url).func, slug_route)

    def test_invalid_slug_route_raises_no_reverse_match(self):
        invalid_slugs = (
            '1411rwasf123412341234',
            '.4/24]['
        )
        for slug in invalid_slugs:
            with self.subTest(case=slug):
                with self.assertRaises(NoReverseMatch):
                    url = reverse('routing:slug_route', args=[slug])
