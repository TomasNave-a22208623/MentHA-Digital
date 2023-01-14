from django import template
from datetime import datetime

register = template.Library()


@register.simple_tag
def verifica_se_tem_valores(val, texto):
    temp = str(val)
    if len(temp) > 2 and val is not None:
        return temp
    else:
        return texto
