# wagtail-simple-seo

Lightweight SEO metadata and social sharing support for Wagtail.

The package provides a small, reusable SEO layer for Wagtail sites without adding SEO scoring, structured-data builders, preview modes, or other heavyweight features.

## Features

- SEO title with page and site-name fallback
- Meta description with configurable page-field fallbacks and a site-wide default
- Canonical URL override with automatic page URL fallback
- Open Graph metadata
- Twitter/X card metadata
- Page-specific social image with configurable fallbacks and a site-wide default
- Absolute social image URLs
- Optional `noindex, follow`
- Reusable source lists that page types can override

## Installation

Install the package and add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ...
    "wagtail_simple_seo",
]
```

Run migrations:

```console
python manage.py migrate
```

## Page models

Use `SeoMixin` with a Wagtail page model:

```python
from wagtail.models import Page
from wagtail_simple_seo.models import SeoMixin

class BasicPage(SeoMixin, Page):
    pass
```

The mixin adds `canonical_url`, `og_image`, and `noindex`, and provides reusable Promote-tab panels:

```python
promote_panels = SeoMixin.seo_panels
```

Page types can customize fallback sources:

```python
class BasicPage(SeoMixin, Page):
    seo_description_sources = ["search_description", "intro"]
    seo_image_sources = ["og_image", "image"]
```

Supported source lists are `seo_pagetitle_sources`, `seo_description_sources`, `canonical_url_sources`, and `seo_image_sources`.

## Site-wide defaults

In Wagtail admin, open **Settings → SEO** to configure the default meta description and default social image.

## Templates

Load the template tag and render metadata inside `<head>`:

```django
{% load seo_tags %}
{% seo_meta page %}
```

## Default fallback behavior

```text
Title
seo_title
→ page title + site name

Description
search_description
→ site-wide default description
→ empty

Canonical URL
canonical_url
→ page.get_full_url()

Social image
og_image
→ site-wide default social image
→ none
```

Individual page types can insert their own fields into these chains by overriding the source lists.

## Scope

The package intentionally does not provide SEO scoring, search-result previews, organization structured data, schema builders, or content analysis. It is intended to cover the common metadata needs of Wagtail sites with a small API and minimal maintenance overhead.
