from django.test import SimpleTestCase


class TestEchoView(SimpleTestCase):
    """Test echo view and template rendering"""

    def setUp(self):
        self.url = '/template/echo/'

    def test_echo_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, template_name='echo.html')

    def test_get_without_parameters_returns_statement_is_empty(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'statement is empty',
                            status_code=200, html=True)

    def test_get_with_x_print_statement_header_set(self):
        response = self.client.get(self.url, HTTP_X_PRINT_STATEMENT='test')
        self.assertContains(response, 'statement is test',
                            status_code=200, html=True)

    def test_get_with_parameters(self):
        TESTCASES = (
            ('?a=1', 'get a: 1 statement is empty'),
            ('?c=2', 'get c: 2 statement is empty'),
            ('?b=3&d=4', 'get b: 3 d: 4 statement is empty'),
        )
        for query, expected in TESTCASES:
            with self.subTest(case=query, expected=expected):
                response = self.client.get(self.url + query)
                self.assertContains(response, expected,
                                    status_code=200, html=True)

    def test_post_without_parameters_returns_statement_is_empty(self):
        response = self.client.post(self.url)
        self.assertContains(response, 'statement is empty',
                            status_code=200, html=True)

    def test_post_with_x_print_statement_header_set(self):
        response = self.client.post(self.url, HTTP_X_PRINT_STATEMENT='test')
        self.assertContains(response, 'statement is test',
                            status_code=200, html=True)

    def test_post_with_parameters(self):
        TESTCASES = (
            ({'b': 1}, 'post b: 1 statement is empty'),
            ({'d': 3}, 'post d: 3 statement is empty'),
            ({'a': 2, 'b': 4}, 'post a: 2 b: 4 statement is empty'),
        )
        for data, expected in TESTCASES:
            with self.subTest(case=data, expected=expected):
                response = self.client.post(self.url, data=data)
                self.assertContains(response, expected,
                                    status_code=200, html=True)
