from django import template

register = template.Library()

@register.simple_tag
def query_transform(request):
    updated = request.GET.copy()
    if 'page' in updated:
        updated.pop('page')
    return updated.urlencode()

@register.filter(name='addcss')
def addcss(field, css):
   return field.as_widget(attrs={"class":css})