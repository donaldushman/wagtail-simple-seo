# wagtail-simple-seo

Lightweight SEO metadata and social sharing support for Wagtail.

`wagtail-simple-seo` provides a small, reusable SEO layer for Wagtail sites without adding SEO scoring, structured-data builders, preview modes, or other heavyweight features.

It is designed for sites that need standard page metadata and sensible fallbacks while keeping SEO configuration simple for developers and content editors.

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
- Migration-friendly field definitions for existing Wagtail sites

## Requirements

- Python 3.10+
- Django 5.2, 6.0, or 6.1 (including 6.1.2)
- Wagtail 7.2 through 8.x

Django 6.x requires Python 3.12+. For Django 6.1, use Wagtail 8.0+.

## Installation

Install the package:

```console
pip install wagtail-simple-seo
```

Add it to `INSTALLED_APPS`:

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

The mixin adds:

- `canonical_url`
- `og_image`
- `noindex`

Wagtail already provides `seo_title` and `search_description`.

The mixin also provides reusable Promote-tab panels:

```python
promote_panels = SeoMixin.seo_panels
```

### Custom fallback sources

Page types can customize the fields used to resolve metadata:

```python
class BasicPage(SeoMixin, Page):
    seo_description_sources = [
        "search_description",
        "intro",
    ]

    seo_image_sources = [
        "og_image",
        "image",
    ]
```

Supported source lists are:

- `seo_pagetitle_sources`
- `seo_description_sources`
- `canonical_url_sources`
- `seo_image_sources`

The first populated source is used.

This allows page-specific fields to participate in SEO metadata without requiring additional SEO fields or duplicated content.

### Custom Promote panels

Sites that already customize Wagtail's Promote tab can use the mixin's panel groups independently:

```python
promote_panels = (
    list(SeoMixin.seo_meta_panels)
    + list(SeoMixin.seo_menu_panels)
)
```

Alternatively, a page type can define its own metadata panel and use only the navigation panels:

```python
from wagtail.admin.panels import FieldPanel, MultiFieldPanel


promote_panels = [
    MultiFieldPanel(
        [
            FieldPanel("slug"),
            FieldPanel("seo_title"),
            FieldPanel("search_description"),
            FieldPanel("canonical_url"),
            FieldPanel("noindex"),
            FieldPanel("og_image"),
        ],
        heading="Search and Social Previews",
    ),
] + list(SeoMixin.seo_menu_panels)
```

This is useful when a project uses a custom panel for fields such as `search_description`.

When defining custom Promote panels, avoid adding a field explicitly and then including a panel group that already contains the same field.

## Site-wide defaults

In Wagtail admin, open **Settings → SEO** to configure:

- Default meta description
- Default social image

These values are used when a page does not provide its own value through its configured source list.

## Templates

Load the template tag and render the metadata inside `<head>`:

```django
{% load seo_tags %}

<head>
    {% seo_meta page %}
    ...
</head>
```

The tag renders:

- Page title
- Meta description
- Canonical URL
- Open Graph title
- Open Graph description
- Open Graph URL
- Open Graph site name
- Open Graph image, when available
- Twitter/X card metadata
- Robots directive when `noindex` is enabled

A robots meta tag is emitted only when `noindex` is enabled for the page.

## Default fallback behavior

### Title

```text
seo_title
→ page title + site name
```

### Description

```text
search_description
→ site-wide default description
→ empty
```

### Canonical URL

```text
canonical_url
→ page.get_full_url()
```

### Social image

```text
og_image
→ site-wide default social image
→ none
```

Individual page types can insert their own fields into these chains by overriding the corresponding source lists.

For example:

```python
seo_image_sources = [
    "og_image",
    "image",
]
```

produces:

```text
og_image
→ image
→ site-wide default social image
→ none
```

## Generated metadata

For a typical page, the generated markup is similar to:

```html
<title>Example Page | Example Site</title>
<meta name="description" content="Example description">
<link rel="canonical" href="https://example.com/example/">

<meta property="og:title" content="Example Page | Example Site">
<meta property="og:description" content="Example description">
<meta property="og:url" content="https://example.com/example/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Example Site">
<meta property="og:image" content="https://example.com/media/images/example.jpg">

<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Example Page | Example Site">
<meta name="twitter:description" content="Example description">
<meta name="twitter:image" content="https://example.com/media/images/example.jpg">
```

When no social image is available, the image tags are omitted and the Twitter/X card uses `summary`.

When `noindex` is enabled:

```html
<meta name="robots" content="noindex, follow">
```

No robots meta tag is emitted by default.

## Migrating an existing site

`wagtail-simple-seo` is designed to support incremental migration from an existing SEO implementation.

Because Wagtail already provides `seo_title` and `search_description`, and many SEO implementations use similar fields for canonical URLs and social images, existing page data can often be preserved without significant schema changes.

The exact migration process depends on the existing implementation. Always review generated migrations before applying them.

### 1. Install the package

Add `wagtail_simple_seo` to `INSTALLED_APPS` alongside the site's existing SEO application, if applicable:

```python
INSTALLED_APPS = [
    # ...
    "existing_seo_app",
    "wagtail_simple_seo",
]
```

Run the package migration:

```console
python manage.py migrate wagtail_simple_seo
```

Keeping both applications installed temporarily allows the migration to be completed incrementally.

### 2. Update page models

Replace the existing SEO mixin or fields with `SeoMixin`:

```python
from wagtail.models import Page
from wagtail_simple_seo.models import SeoMixin


class BasicPage(SeoMixin, Page):
    pass
```

The mixin provides:

- `canonical_url`
- `og_image`
- `noindex`

Wagtail provides `seo_title` and `search_description`.

If the existing page model already contains compatible `canonical_url` and `og_image` fields, Django may be able to preserve them without database schema changes.

Create migrations and review them before applying:

```console
python manage.py makemigrations
```

A typical migration may only need to add the `noindex` field, but this depends on the existing models and field definitions.

Once the generated migration has been reviewed:

```console
python manage.py migrate
```

### 3. Review custom Promote panels

If a page model defines its own `promote_panels`, check for fields that are also included in `SeoMixin.seo_meta_panels`.

For example, explicitly adding `search_description` and then appending `SeoMixin.seo_meta_panels` will display the field twice.

Use either the supplied panel groups or construct a custom metadata panel as described above.

### 4. Update templates

Replace the site's existing metadata rendering with:

```django
{% load seo_tags %}
{% seo_meta page %}
```

Place the tag inside the document `<head>`.

Remove old metadata, structured-data, or schema template includes only after determining whether the site still requires that functionality.

`wagtail-simple-seo` does not provide structured-data or schema-building features.

### 5. Review site-wide settings

An existing SEO implementation may store information beyond page metadata, including:

- Organization descriptions
- Phone numbers
- Addresses
- Social accounts
- Structured-data configuration
- Other site-wide metadata

Review these settings before removing the existing implementation.

Content that is part of the website itself, such as contact information or addresses, can generally be moved to the project's own Wagtail site settings.

Configure the metadata defaults provided by `wagtail-simple-seo` under **Settings → SEO**:

- Default meta description
- Default social image

### 6. Remove the previous implementation

Once application code and templates no longer depend on the previous SEO implementation:

1. Remove the old application from `INSTALLED_APPS`.
2. Remove its Python dependency, if applicable.
3. Run Django's system checks and test suite.

For example:

```console
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

Old database tables do not necessarily need to be removed as part of the application migration. Database cleanup can be handled separately after the migration has been verified.

## Scope

The package intentionally does not provide:

- SEO scoring or content analysis
- Search-result previews
- Organization structured data
- Schema builders
- Organization contact or address management
- Social account configuration

These concerns are intentionally left to the application or to specialized packages.

`wagtail-simple-seo` is intended to cover the common metadata needs of Wagtail sites with a small API, predictable behavior, and minimal maintenance overhead.
