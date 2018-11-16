from django import template

register = template.Library()

@register.simple_tag
def query_transform(request, remove = 'page'):
    updated = request.GET.copy()
    if remove in updated:
        updated.pop(remove)
    return updated.urlencode()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})