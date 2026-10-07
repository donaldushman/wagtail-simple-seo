from django import template
from wagtail_simple_seo.utils import (
    get_canonical_url, get_seo_description, get_seo_image_url,
    get_seo_site_name, get_seo_title,
)

register = template.Library()

@register.inclusion_tag("wagtail_simple_seo/seo_meta.html")
def seo_meta(page):
    return {
        "seo_title": get_seo_title(page),
        "seo_description": get_seo_description(page),
        "seo_canonical_url": get_canonical_url(page),
        "seo_site_name": get_seo_site_name(page),
        "seo_image_url": get_seo_image_url(page),
        "seo_noindex": getattr(page, "noindex", False),
    }
