"""VK API client that calculates age distribution of user's friends"""
import logging
import re
from collections import Counter
from datetime import date
from typing import List, Tuple, Optional, Dict, Any

import requests

# VK API service token
ACCESS_TOKEN = 'cf5c063dcf5c063dcf5c063dcacf2f3021ccf5ccf5c063d9042035ee1dacc55caec56d9'

# Configure logging
friends_logger = logging.getLogger('friends.py')
friends_logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('INFO')
# Write new log on each run
file_handler = logging.FileHandler(filename='debug.log',
                                   mode='w', encoding='utf-8')
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

friends_logger.addHandler(console_handler)
friends_logger.addHandler(file_handler)


def get_user_id_by_username_or_id(uid: str) -> Optional[int]:
    """Return user_id.

    Gets user_id by username or id.
    Returns None if no user was found for specified username or id.

    API Method docs: https://vk.com/dev/users.get

    VK API version: 5.71
    """
    if not uid:
        friends_logger.warning('No username or id provided')
        return None

    request = requests.get(f"https://api.vk.com/method/users.get?v=5.71"
                           f"&access_token={ACCESS_TOKEN}&user_ids={uid}")
    friends_logger.debug("Sending %s request: '%s'",
                         request.request.method, request.request.url)
    request.raise_for_status()
    response = request.json()
    try:
        user_id = response['response'][0]['id']
        friends_logger.debug("Got response: '%s'", str(response))
        if not uid.isnumeric():
            friends_logger.info("Got user_id %d for uid '%s'", user_id, uid)
        return user_id
    except (KeyError, IndexError):
        friends_logger.error("Error getting user id for uid='%s'. "
                             "Response: '%s'", uid, str(response))
        return None


def get_user_friends(
        user_id: int, *fields: str
) -> Optional[List[Dict[str, Any]]]:
    """Return list of user's friends.

    Gets user's friends with their attributes.
    Returns list of friends or None if unable to get data for user_id.

    :param user_id: User id.
    :param fields: Additional attributes of friend, 'bdate' if not provided.

    API Method docs: https://vk.com/dev/friends.get

    VK API version: 5.71
    """
    if not fields:
        fields = ('bdate',)

    request = requests.get(f"https://api.vk.com/method/friends.get?v=5.71"
                           f"&access_token={ACCESS_TOKEN}&user_id="
                           f"{user_id}&fields={fields}")
    friends_logger.debug("Sending %s request: '%s'",
                         request.request.method, request.request.url)
    request.raise_for_status()
    response = request.json()
    try:
        friends_list = response['response']['items']
        friends_logger.debug("Got response: '%s'", str(response))
        friends_logger.info('Got %d friends total', len(friends_list))
        return friends_list
    except KeyError:
        friends_logger.error("Error getting friends for user "
                             "with user_id='%s'. Response: '%s'",
                             user_id, str(response))
        return None


def get_friends_id_age_pairs(
        friends_list: List[Dict[str, Any]]
) -> List[Tuple[int, int]]:
    """Return list of friends' ids and ages.

    :param friends_list: List of friends' data dictionaries.
    """
    id_age_pairs = []
    for friend in friends_list:
        if 'bdate' in friend.keys():
            age = _get_age_from_birthdate(friend['bdate'])
            if age:
                id_age_pairs.append((friend['id'], age))
    return id_age_pairs


def _get_age_from_birthdate(birthdate: str) -> Optional[int]:
    """Return age for a given full birthdate or None if there is no year
    in birthdate.

    Ignores day and month of birth in calculation.
    """
    if not re.match(r'\d{1,2}\.\d{1,2}\.\d{4}$', birthdate):
        return None
    birthyear = int(birthdate[-4:])
    age = date.today().year - birthyear
    return age


def calc_age(uid: str) -> List[Tuple[int, int]]:
    """Return list of (age, number_of_friends_of_this_age) pairs
    ordered by second key descending first, then by first key ascending.
    """
    user_id = get_user_id_by_username_or_id(uid)
    if not user_id:
        return []
    friends_list = get_user_friends(user_id)
    if not friends_list:
        return []
    friends_list_with_ages = get_friends_id_age_pairs(friends_list)
    friends_logger.info('Calculated ages for %d friends',
                        len(friends_list_with_ages))
    counted_ages = Counter([
        age
        for friend_id, age in sorted(friends_list_with_ages,
                                     key=lambda x: x[1])
    ])
    return sorted(list(counted_ages.items()),
                  key=lambda x: x[1], reverse=True)


if __name__ == '__main__':
    res = calc_age('reigning')
    friends_logger.info('Result: %s', res)
    print(res)
