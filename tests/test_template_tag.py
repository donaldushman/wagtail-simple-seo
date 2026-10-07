from types import SimpleNamespace
from unittest.mock import patch

from django.template import Context, Template
from django.test import SimpleTestCase


class SeoMetaTagTests(SimpleTestCase):
    @patch("wagtail_simple_seo.templatetags.seo_tags.get_seo_image_url")
    @patch("wagtail_simple_seo.templatetags.seo_tags.get_seo_site_name")
    @patch("wagtail_simple_seo.templatetags.seo_tags.get_canonical_url")
    @patch("wagtail_simple_seo.templatetags.seo_tags.get_seo_description")
    @patch("wagtail_simple_seo.templatetags.seo_tags.get_seo_title")
    def test_meta_output(
        self,
        get_title,
        get_description,
        get_canonical,
        get_site_name,
        get_image_url,
    ):
        get_title.return_value = "About | Example"
        get_description.return_value = "About Example"
        get_canonical.return_value = "https://example.com/about/"
        get_site_name.return_value = "Example"
        get_image_url.return_value = "https://example.com/media/social.jpg"

        page = SimpleNamespace(noindex=True)
        rendered = Template(
            "{% load seo_tags %}{% seo_meta page %}"
        ).render(Context({"page": page}))

        self.assertIn("<title>About | Example</title>", rendered)
        self.assertIn('content="About Example"', rendered)
        self.assertIn('rel="canonical" href="https://example.com/about/"', rendered)
        self.assertIn('property="og:image" content="https://example.com/media/social.jpg"', rendered)
        self.assertIn('content="noindex, follow"', rendered)
