from django import template

register = template.Library()

# Status order for progress tracking
STATUS_ORDER = ['pending', 'confirmed', 'processing', 'ready', 'delivered']

@register.filter
def split(value, delimiter=','):
    return value.split(delimiter)

@register.filter
def status_reached(current_status, check_status):
    """Returns True if current_status is at or past check_status in the workflow."""
    try:
        current_idx = STATUS_ORDER.index(current_status)
        check_idx = STATUS_ORDER.index(check_status)
        return current_idx >= check_idx
    except ValueError:
        return False
