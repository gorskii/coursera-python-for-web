import json

import pytest


@pytest.fixture
def valid_item_json():
    return json.dumps({
        'title': 'Сыр "Российский"',
        'description': 'Очень вкусный сыр, да еще и российский.',
        'price': 100
    })


@pytest.fixture
def invalid_item_json():
    return '\
        {\
            "title": "Сыр \\\"Российский\\\"",\
            "description": "Очень вкусный сыр, да еще и российский.",\
            "price": 100\
    '
