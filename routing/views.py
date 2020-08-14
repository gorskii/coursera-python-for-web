from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_safe, require_POST


@require_safe
def simple_route(request):
    """Return empty response.

    Only GET method allowed, so using @require_safe decorator.
    """
    return HttpResponse(status=200)


def slug_route(request, slug):
    """Return slug"""
    return HttpResponse(slug, status=200)


def sum_route(request, first, second):
    """Return first + second"""
    result = int(first) + int(second)
    return HttpResponse(result, status=200)


@require_safe
def sum_get_method(request):
    """Return a + b. a and b passed through request.GET attributes.

    Only GET method allowed, so using @require_safe decorator.
    """
    try:
        a = request.GET['a']
        b = request.GET['b']
        result = int(a) + int(b)
    except KeyError as e:
        return HttpResponseBadRequest(
            f'Missing required argument(s): {e.args[0]}'
        )
    except ValueError:
        return HttpResponseBadRequest(
            "Invalid argument(s) value. Both 'a' and 'b' should be numbers."
        )
    return HttpResponse(result, status=200)


@require_POST
@csrf_exempt
def sum_post_method(request):
    """Return a + b. a and b passed through request.POST attributes.

    Only POST method allowed, so using @require_POST decorator.

    Add @csrf_exempt decorator to allow requests without X-CSRFToken
    header or CSRF token cookie.
    """
    try:
        a = request.POST['a']
        b = request.POST['b']
        result = int(a) + int(b)
    except KeyError as e:
        return HttpResponseBadRequest(
            f'Missing required argument(s): {e.args[0]}'
        )
    except ValueError:
        return HttpResponseBadRequest(
            "Invalid argument(s) value. Both 'a' and 'b' should be numbers."
        )
    return HttpResponse(result, status=200)
