from django.http import HttpResponse
from django.views.decorators.http import require_safe


@require_safe
def simple_route(request):
    """Return empty response.

    Only GET method allowed, so using @require_safe decorator.
    """
    return HttpResponse(status=200)


def slug_route(request, slug):
    """Return slug"""
    return HttpResponse(slug, status=200)
