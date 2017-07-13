from django import template

register = template.Library()

def widget_type(ob):
	return ob.__class__.__name__

register.filter('widget_type', widget_type)