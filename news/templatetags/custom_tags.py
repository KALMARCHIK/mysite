

from django import template

from news.models import Rubric

register = template.Library()


@register.simple_tag()
def rubric_all():
    return Rubric.objects.all()
