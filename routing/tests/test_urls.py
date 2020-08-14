from django.test import SimpleTestCase
from django.urls import reverse, resolve, NoReverseMatch

from routing.views import (
    simple_route,
    slug_route,
    sum_route,
    sum_get_method,
    sum_post_method,
)


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


class TestSumRouteUrls(SimpleTestCase):
    """Test urls resolving sum_route path"""

    def test_sum_route_resolves(self):
        url = reverse(
            'routing:sum_route', kwargs={'first': '1', 'second': '-2'}
        )
        self.assertEqual(resolve(url).func, sum_route)

    def test_invalid_sum_route_raises_no_reverse_match(self):
        invalid_kwargs = (
            {'first': '1', 'second': 'b'},
            {'first': 'a', 'second': '2'},
        )
        for kwargs in invalid_kwargs:
            with self.subTest(case=kwargs):
                with self.assertRaises(NoReverseMatch):
                    reverse('routing:sum_route', kwargs=kwargs)


class TestSumGetMethodUrls(SimpleTestCase):
    """Test urls resolving sum_get_method path"""

    def test_sum_get_method_resolves(self):
        url = reverse('routing:sum_get_method')
        self.assertEqual(resolve(url).func, sum_get_method)


class TestSumPostMethodUrls(SimpleTestCase):
    """Test urls resolving sum_post_method path"""

    def test_sum_post_method_resolves(self):
        url = reverse('routing:sum_post_method')
        self.assertEqual(resolve(url).func, sum_post_method)
