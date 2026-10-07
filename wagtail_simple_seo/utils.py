from typing import Optional
from wagtail.images.models import AbstractImage
from .models import SEOSettings

def get_first_value(obj, sources):
    for attr in sources:
        if hasattr(obj, attr):
            value = getattr(obj, attr)
            if value:
                return value
    return None

def get_seo_site(page):
    return page.get_site()

def get_seo_site_name(page) -> str:
    site = get_seo_site(page)
    return site.site_name if site else ""

def get_seo_title(page) -> str:
    sources = getattr(page, "seo_pagetitle_sources", ["seo_title"])
    title = get_first_value(page, sources)
    if title:
        return str(title)
    site_name = get_seo_site_name(page)
    return f"{page.title} | {site_name}" if site_name else page.title

def get_seo_description(page) -> str:
    sources = getattr(page, "seo_description_sources", ["search_description"])
    description = get_first_value(page, sources)
    if description:
        return str(description)
    settings = SEOSettings.for_site(get_seo_site(page))
    return settings.default_description or ""

def get_canonical_url(page) -> str:
    sources = getattr(page, "canonical_url_sources", ["canonical_url"])
    url = get_first_value(page, sources)
    return str(url) if url else (page.get_full_url() or "")

def get_seo_image(page) -> Optional[AbstractImage]:
    sources = getattr(page, "seo_image_sources", ["og_image"])
    for attr in sources:
        if hasattr(page, attr):
            image = getattr(page, attr)
            if isinstance(image, AbstractImage):
                return image
    settings = SEOSettings.for_site(get_seo_site(page))
    return settings.default_social_image

def get_seo_image_url(page) -> str:
    image = get_seo_image(page)
    if not image:
        return ""
    url = image.get_rendition("original").url
    if url.startswith(("http://", "https://")):
        return url
    site = get_seo_site(page)
    if not site:
        return url
    return f"{site.root_url.rstrip('/')}/{url.lstrip('/')}"
