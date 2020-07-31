import unittest
from unittest.mock import patch, Mock

from req.friends import (
    get_user_id_by_username_or_id,
    get_user_friends,
    get_friends_id_age_pairs,
    _get_age_from_birthdate,
    calc_age,
)


class TestFriends(unittest.TestCase):

    def setUp(self) -> None:
        self.username = 'reigning'
        self.user_id = 150617534
        self.friends_list = [
            {'id': 6477, 'first_name': 'Oksana', 'last_name': 'Ozernaya'},
            {'id': 96163, 'first_name': 'Sergey', 'last_name': 'Kushlevich',
             'bdate': '5.3.1986'},
            {'id': 135863, 'first_name': 'Alexander', 'last_name': 'Gorny', },
            {'id': 198261, 'first_name': 'Sveta', 'last_name': 'Snegireva',
             'bdate': '27.4'},
            {'id': 274123, 'first_name': 'Ilya', 'last_name': 'Penyaev',
             'bdate': '20.7.1989'},
            {'id': 5673757, 'first_name': 'Evgenia',
             'last_name': 'Chernobrovkina', 'bdate': '5.5.1994'},
            {'id': 5844771, 'first_name': 'Adelaida',
             'last_name': 'Titengauzen', 'bdate': '13.3.1994'},
        ]
        self.friends_count = 7

    def test_get_user_id(self):
        cases = (
            (self.username, self.user_id),
            (str(self.user_id), self.user_id),
            ('', None),
            ('d', None),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                self.assertEqual(get_user_id_by_username_or_id(case), expected)

    @patch('req.friends.requests.get')
    def test_get_user_friends(self, mocked_get):
        mocked_response = Mock()
        mocked_get.return_value = mocked_response
        mocked_response.request.method = 'GET'
        mocked_response.request.url = (
            f"https://api.vk.com/method/friends.get?v=5.71"
            f"&access_token=test"
            f"&user_id={self.user_id}&fields={'bdate'}"
        )
        mocked_response.json.return_value = {
            'response': {
                "count": self.friends_count,
                "items": self.friends_list
            }
        }
        self.assertEqual(get_user_friends(self.user_id), self.friends_list)

    def test_get_user_friends_for_invalid_id(self):
        self.assertEqual(get_user_friends(0), None)

    def test_get_friends_id_age_pairs(self):
        expected = [
            (96163, 34),
            (274123, 31),
            (5673757, 26),
            (5844771, 26),
        ]
        self.assertEqual(get_friends_id_age_pairs(self.friends_list), expected)

    @patch('req.friends.get_user_friends')
    @patch('req.friends.get_user_id_by_username_or_id')
    def test_calc_age(self, mocked_get_id, mocked_get_friends):
        mocked_get_id.return_value = self.user_id
        mocked_get_friends.return_value = self.friends_list
        expected = [
            (26, 2),
            (31, 1),
            (34, 1),
        ]
        self.assertEqual(calc_age(self.username), expected)

    def test_calc_age_with_invalid_uid(self):
        self.assertEqual(calc_age(''), [])

    def test_calc_age_for_user_with_no_friends(self):
        self.assertEqual(calc_age('durov'), [])

    def test_get_age_from_birthdate(self):
        from datetime import date
        current_year = date.today().year
        cases = (
            ('', None),
            ('1994', None),
            ('1.1', None),
            ('12.12.12412', None),
            ('12.12.1990', current_year - 1990),
            ('11.11.111', None),
            ('1.1.2000', current_year - 2000),
        )
        for case, expected in cases:
            with self.subTest(case=case):
                self.assertEqual(_get_age_from_birthdate(case), expected)


if __name__ == '__main__':
    unittest.main()
