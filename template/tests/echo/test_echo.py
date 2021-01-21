from django.test import SimpleTestCase


class TestEchoView(SimpleTestCase):
    """Test echo view"""

    def setUp(self):
        self.url = '/template/echo/'

    def test_echo_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, template_name='echo.html')

    def test_get_without_parameters_returns_statement_is_empty(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'statement is empty',
                            status_code=200, html=True)

    def test_post_without_parameters(self):
        pass

    def test_get_with_x_print_statement_header_set(self):
        pass

    def test_get_with_parameters(self):
        pass
