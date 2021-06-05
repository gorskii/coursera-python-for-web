import json
from json.decoder import JSONDecodeError

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Item, Review


@method_decorator(csrf_exempt, name='dispatch')
class AddItemView(View):
    """View для создания товара."""

    def post(self, request):
        try:
            document = json.loads(request.body)
        except JSONDecodeError as exc:
            return JsonResponse({'errors': exc.msg}, status=400)

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
