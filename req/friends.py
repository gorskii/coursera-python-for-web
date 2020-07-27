"""VK API client that calculates age distribution of user's friends"""
import logging
from typing import List, Tuple, Optional

import requests

# VK API service token
ACCESS_TOKEN = 'cf5c063dcf5c063dcf5c063dcacf2f3021ccf5ccf5c063d9042035ee1dacc55caec56d9'

# Configure logging
friends_logger = logging.getLogger(__name__)
friends_logger.setLevel("DEBUG")

console_handler = logging.StreamHandler()
console_handler.setLevel("WARNING")

file_handler = logging.FileHandler(filename='debug.log')
file_handler.setLevel("DEBUG")

formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

friends_logger.addHandler(console_handler)
friends_logger.addHandler(file_handler)


def get_user_id_by_username_or_id(uid: str) -> Optional[int]:
    """Return user_id

    Get user_id by username or id

    Method docs: https://vk.com/dev/users.get

    VK API version: 5.71
    """
    request = requests.get(f"https://api.vk.com/method/users.get?v=5.71"
                           f"&access_token={ACCESS_TOKEN}&user_ids={uid}")
    friends_logger.debug("Sending %s request: '%s'",
                         request.request.method, request.request.url)
    request.raise_for_status()
    response = request.json()
    try:
        user_id = response.get('response')[0]['id']
        friends_logger.debug("Got response: '%s'", str(response))
        return user_id
    except (IndexError, TypeError):
        friends_logger.warning("Error getting user id for uid='%s'. "
                               "Response: '%s'", uid, str(response))
        return None


def calc_age(uid: str) -> List[Tuple[int, int]]:
    """Return list of (age, number_of_friends_of_this_age) pairs
    ordered in descending order by second key first, then in ascending
    order by first key.

    """
    user_id = get_user_id_by_username_or_id(uid)
    if user_id is None:
        return []

    return []


if __name__ == '__main__':
    res = calc_age('reigning')
    print(res)
