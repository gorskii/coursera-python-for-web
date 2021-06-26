import json

import pytest

from somemart.models import Item, Review

pytestmark = pytest.mark.django_db


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


class TestAddItemView:
    url = '/api/v1/goods/'

    def test_post_item(self, client, valid_item_json):
        """/api/v1/goods/ (POST) сохраняет товар в базе."""
        response = client.post(self.url, data=valid_item_json,
                               content_type='application/json')

        assert response.status_code == 201
        document = response.json()
        item = Item.objects.get(pk=document['id'])
        assert item.title == 'Сыр "Российский"'
        assert item.description == 'Очень вкусный сыр, да еще и российский.'
        assert item.price == 100

    def test_invalid_json_not_processed(self, client, invalid_item_json):
        response = client.post(self.url, data=invalid_item_json,
                               content_type='application/json')

        assert response.status_code == 400
        assert 'errors' in response.json()
        assert not Item.objects.all().exists()

    def test_zero_price_is_not_valid(self, client):
        data = json.dumps({
            'title': 'Zero-priced item',
            'description': 'test item description',
            'price': 0,
        })
        response = client.post(self.url, data=data,
                               content_type='application/json')

        assert response.status_code == 400

    def test_too_big_price_is_not_valid(self, client):
        data = json.dumps({
            'title': 'Too expensive item',
            'description': 'test item description',
            'price': 1_000_001,
        })
        response = client.post(self.url, data=data,
                               content_type='application/json')

        assert response.status_code == 400

    def test_empty_title_is_not_valid(self, client):
        pass
