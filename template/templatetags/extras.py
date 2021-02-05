from django import template

register = template.Library()


@register.filter
def inc(number, increment):
    """Increment number by given increment"""
    return int(number) + int(increment)


@register.simple_tag
def division(first, second, to_int=False):
    """Divide first number by second number

    If to_int=True cast result to int.
    """
    try:
        res = int(first) / int(second)
    except ZeroDivisionError as e:
        return f'Error: {e}'
    return int(res) if to_int else res
