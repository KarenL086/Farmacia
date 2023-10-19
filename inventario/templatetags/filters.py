from django import template

register = template.Library()

@register.filter
def gruposList(user, nombreGrupo):
    return user.groups.filter(name=nombreGrupo).exists()
