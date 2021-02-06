from django.test import SimpleTestCase


class TestFilterView(SimpleTestCase):
    """Test filters view and custom template tag and filter"""

    def setUp(self):
        self.url = '/template/filters/'

    def test_filters_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, template_name='filters.html')

    def test_inc_filter_rendering(self):
        TESTCASES = (
            ('?a=1', '11'),
            ('?a=0', '10'),
            ('?a=-12', '-2'),
        )
        for query, expected in TESTCASES:
            with self.subTest(query=query, expected=expected):
                response = self.client.get(self.url + query)
                self.assertContains(response, expected)

    def test_division_tag_rendering(self):
        TESTCASES = (
            ('?a=3&b=2', '1', '1.5'),
            ('?a=6&b=2', '3', '3.0'),
            ('?a=7&b=-2', '-3', '-3.5'),
        )
        for query, expected_int, expected_float in TESTCASES:
            with self.subTest(query=query,
                              expected_int=expected_int,
                              expected_float=expected_float):
                response = self.client.get(self.url + query)
                self.assertContains(response, expected_int)
                self.assertContains(response, expected_float)
