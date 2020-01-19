from django import template

from oscar.core.loading import get_model

register = template.Library()
Range = get_model('offer', 'range')


@register.simple_tag(name="range_list")
def get_public_range():
    """
    Return a list of all public ranges.
    """
    return Range.objects.filter(is_public=True)
