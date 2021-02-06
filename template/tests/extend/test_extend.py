from django.test import SimpleTestCase


class TestExtendView(SimpleTestCase):
    """Test extend view and template inheritance"""

    def setUp(self):
        self.url = '/template/extend/'

    def test_extend_template_used(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, template_name='extend.html')

    def test_extend_template_inherits_base_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, template_name='base.html')

    def test_parent_block_content_is_rendered(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Simple text a')
        self.assertContains(response, 'Simple text b')

    def test_passed_arguments_rendered(self):
        TESTCASES = (
            ('?a=3&b=2', '3', '2'),
            ('?a=2&b=-1', '2', '-1'),
            ('?a=9&b=4', '9', '4'),
        )
        for query, expected_a, expected_b in TESTCASES:
            with self.subTest(query=query,
                              expected_a=expected_a,
                              expected_b=expected_b):
                response = self.client.get(self.url + query)
                self.assertContains(response, expected_a)
                self.assertContains(response, expected_b)

    def test_extend_with_no_arguments_not_render_none(self):
        response = self.client.get(self.url)
        self.assertNotContains(response, 'None')
