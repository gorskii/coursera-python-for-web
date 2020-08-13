from django.test import SimpleTestCase
from django.urls import reverse


class TestSimpleRouteView(SimpleTestCase):
    """Test simple_route view"""

    def test_get_simple_route_root(self):
        response = self.client.get(reverse('routing:simple_route'))

        self.assertEqual(response.status_code, 200)

    def test_get_simple_route_contents_404(self):
        response = self.client.get(
            reverse('routing:simple_route') + 'anything'
        )

        self.assertEqual(response.status_code, 404)

    def test_simple_route_non_get_methods_not_allowed(self):
        cases = (
            ('post', self.client.post),
            ('put', self.client.put),
        )
        for case, request_method in cases:
            with self.subTest(case=case):
                response = request_method(reverse('routing:simple_route'))
                self.assertEqual(response.status_code, 405)


class TestSlugRouteView(SimpleTestCase):
    """Test slug_route view"""

    def test_get_valid_slug_route(self):
        example_slug = 'a-1s_d2'
        response = self.client.get(
            reverse('routing:slug_route', args=[example_slug])
        )

        self.assertEqual(response.content.decode(), example_slug)

    def test_get_invalid_slug_route_returns_404(self):
        invalid_slugs = (
            '1411rwasf123412341234',
            '.4/24]['
        )
        for slug in invalid_slugs:
            with self.subTest(case=slug):
                # Don't know how to test 404 on invalid path using reverse
                url = f'/routing/slug_route/{slug}'
                response = self.client.post(url)
                self.assertEqual(response.status_code, 404)


class TestSumRouteView(SimpleTestCase):
    """Test sum_route view"""

    def test_get_sum_route_with_two_positive_numbers(self):
        url = reverse(
            'routing:sum_route', kwargs={'first': '1', 'second': '2'}
        )
        expected = '3'
        response = self.client.get(url)
        self.assertEqual(response.content.decode(), expected)

    def test_get_sum_route_with_one_negative_number(self):
        url = reverse(
            'routing:sum_route', kwargs={'first': '1', 'second': '-2'}
        )
        expected = '-1'
        response = self.client.get(url)
        self.assertEqual(response.content.decode(), expected)
