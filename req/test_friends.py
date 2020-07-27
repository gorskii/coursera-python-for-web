import unittest
from req.friends import get_user_id_by_username_or_id, ACCESS_TOKEN


class TestFriends(unittest.TestCase):

    def setUp(self) -> None:
        self.token = ACCESS_TOKEN

    def test_get_user_id(self):
        cases = ('reigning', '150617534', '', 'd')
        expected_results = (150617534, 150617534, None, None)
        for case, expected in zip(cases, expected_results):
            with self.subTest(case=case):
                self.assertEqual(get_user_id_by_username_or_id(case), expected)


if __name__ == '__main__':
    unittest.main()
