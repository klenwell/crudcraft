"""
    Custom Form Filters
"""
from bleach import clean


def scrub(value):
    if not value:
        return ''
    return clean(value, tags=[], strip=True)


def strip(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value
