from django.test import TestCase, Client
from django.urls import reverse


class TestSimpleRouteViews(TestCase):
    """Test simple_route views"""

    def setUp(self):
        self.client = Client()

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
