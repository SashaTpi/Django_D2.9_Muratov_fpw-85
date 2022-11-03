from django import template


register = template.Library()

censwords = ['Instagram', 'редиска', 'война', 'ЛГБТ']


@register.filter()
def censor(value):
    for i in censwords:
        if i.find(value):
            value = value.replace(i[1::], "*" * len(i))
    return f'{value}'