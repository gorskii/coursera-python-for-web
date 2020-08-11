from django.http import HttpResponse
from django.views.decorators.http import require_safe


@require_safe
def simple_route(request):
    """Return empty response"""
    return HttpResponse(status=200)
