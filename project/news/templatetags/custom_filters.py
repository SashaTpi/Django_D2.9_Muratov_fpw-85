from django import template


register = template.Library()


@register.filter()
def censor(value):
   censor_list = ['блин', 'редиска', 'скот', 'text']
   if not isinstance(value, str):
      raise ValueError('Фильтр цензурирования применяется только к переменным строкового типа')
   for word in censor_list:
      value = value.replace(word[1:],'*'*(len(word)-1))
   return value