from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def echo(request):
    if request.method == 'POST':
        request_attrs = request.POST
    elif request.method == 'GET':
        request_attrs = request.GET
    else:
        request_attrs = {}

    return render(request, 'echo.html', context={
        'statement_header': request.META.get('HTTP_X_PRINT_STATEMENT'),
        'a': request_attrs.get('a'),
        'b': request_attrs.get('b'),
        'c': request_attrs.get('c'),
        'd': request_attrs.get('d'),
    })


def filters(request):
    return render(request, 'filters.html', context={
        'a': request.GET.get('a', 1),
        'b': request.GET.get('b', 1)
    })


def extend(request):
    return render(request, 'extend.html', context={
        'a': request.GET.get('a'),
        'b': request.GET.get('b')
    })
