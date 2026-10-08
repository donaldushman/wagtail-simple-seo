from wagtail_simple_seo.models import SEOSettings, SeoMixin


def test_seo_settings_uses_unique_site_related_name():
    """Allow wagtail-simple-seo and wagtail-seo to coexist during migration."""
    field = SEOSettings._meta.get_field("site")

    assert field.remote_field.related_name == "simple_seo_settings"


def test_og_image_preserves_legacy_field_metadata():
    """Keep og_image compatible with wagtail-seo to avoid AlterField migrations."""
    field = SeoMixin._meta.get_field("og_image")

    assert field.verbose_name == "Preview image"
    assert field.remote_field.related_name == "+"
    assert field.help_text == (
        "Shown when linking to this page on social media. "
        "If blank, may show an image from the page, or the default from Settings > SEO."
    )