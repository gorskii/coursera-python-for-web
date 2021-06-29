import json
from json.decoder import JSONDecodeError

from django.http import JsonResponse
from django.http.response import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from .models import Item, Review

ITEM_SCHEMA = {
    "$id": "http://example.com/example.json",
    "$schema": "http://json-schema.org/draft-07/schema",
    "title": "Store item (product) schema",
    "type": "object",
    "properties": {
        "title": {
            "title": "Product title",
            "type": "string",
            "maxLength": 64,
            "minLength": 1,
        },
        "description": {
            "title": "Product description",
            "type": "string",
            "maxLength": 1024,
            "minLength": 1,
        },
        "price": {
            "title": "Product price",
            "type": "integer",
            "maximum": 1_000_000,
            "minimum": 1,
        },
    },
    "required": [
        "title",
        "description",
        "price",
    ],
    "additionalProperties": True,
}


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        """Create product."""
        try:
            document = json.loads(request.body)
            validate(document, schema=ITEM_SCHEMA)
        except JSONDecodeError:
            return HttpResponseBadRequest()
        except ValidationError:
            return HttpResponseBadRequest()

        item = Item()
        item.title = document.get('title')
        item.description = document.get('description')
        item.price = document.get('price')
        item.save()

        data = {
            'id': item.pk,
        }

        return JsonResponse(data, status=201)


class PostReviewView(View):
    """View для создания отзыва о товаре."""

    def post(self, request, item_id):
        # Здесь должен быть ваш код
        return JsonResponse(data, status=201)


class GetItemView(View):
    """View для получения информации о товаре.

    Помимо основной информации выдает последние отзывы о товаре, не более 5
    штук.
    """

    def get(self, request, item_id):
        # Здесь должен быть ваш код
        return JsonResponse(data, status=200)
