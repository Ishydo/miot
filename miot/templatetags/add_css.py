from django import template

register = template.Library()

# Tag used to add a class to template widget
@register.filter(name='addclass')
def addclass(value, arg):
    return value.as_widget(attrs={'class': arg})
