from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase

from wagtail_simple_seo.utils import (
    get_canonical_url,
    get_first_value,
    get_seo_description,
    get_seo_site_name,
    get_seo_title,
)


class ResolverTests(SimpleTestCase):
    def test_first_value_uses_first_populated_source(self):
        obj = SimpleNamespace(first="", second="value")
        self.assertEqual(get_first_value(obj, ["first", "second"]), "value")

    def test_title_prefers_seo_title(self):
        page = Mock()
        page.seo_pagetitle_sources = ["seo_title"]
        page.seo_title = "Custom title"
        self.assertEqual(get_seo_title(page), "Custom title")

    def test_title_falls_back_to_page_and_site_name(self):
        page = Mock()
        page.seo_pagetitle_sources = ["seo_title"]
        page.seo_title = ""
        page.title = "About"
        page.get_site.return_value = SimpleNamespace(site_name="Example")
        self.assertEqual(get_seo_title(page), "About | Example")

    def test_canonical_url_prefers_override(self):
        page = Mock()
        page.canonical_url_sources = ["canonical_url"]
        page.canonical_url = "https://example.com/preferred/"
        self.assertEqual(
            get_canonical_url(page),
            "https://example.com/preferred/",
        )

    def test_canonical_url_falls_back_to_full_url(self):
        page = Mock()
        page.canonical_url_sources = ["canonical_url"]
        page.canonical_url = ""
        page.get_full_url.return_value = "https://example.com/about/"
        self.assertEqual(
            get_canonical_url(page),
            "https://example.com/about/",
        )

    def test_site_name_uses_wagtail_site(self):
        page = Mock()
        page.get_site.return_value = SimpleNamespace(site_name="Example")
        self.assertEqual(get_seo_site_name(page), "Example")

    @patch("wagtail_simple_seo.utils.SEOSettings.for_site")
    def test_description_falls_back_to_site_default(self, for_site):
        page = Mock()
        page.seo_description_sources = ["search_description"]
        page.search_description = ""
        page.get_site.return_value = object()
        for_site.return_value = SimpleNamespace(
            default_description="Default description"
        )
        self.assertEqual(
            get_seo_description(page),
            "Default description",
        )
