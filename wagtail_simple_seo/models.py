from django.db import models
from wagtail.models import Site
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting
from wagtail.images import get_image_model_string

class SeoMixin(models.Model):
    canonical_url = models.URLField(
        "Canonical URL", blank=True, max_length=255,
        help_text="Leave blank to use the page's URL.",
    )
    og_image = models.ForeignKey(
        get_image_model_string(),
        verbose_name="Preview image",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=(
            "Shown when linking to this page on social media. "
            "If blank, may show an image from the page, or the default from Settings > SEO."
        ),
    )
    noindex = models.BooleanField(
        default=False, verbose_name="Hide from search engines",
        help_text="Ask search engines not to index this page.",
    )

    seo_description_sources = ["search_description"]
    canonical_url_sources = ["canonical_url"]
    seo_image_sources = ["og_image"]
    seo_pagetitle_sources = ["seo_title"]

    seo_meta_panels = [
        MultiFieldPanel([
            FieldPanel("slug"),
            FieldPanel("seo_title"),
            FieldPanel("search_description"),
            FieldPanel("canonical_url"),
            FieldPanel("noindex"),
            FieldPanel("og_image"),
        ], heading="Search and Social Previews"),
    ]
    seo_menu_panels = [
        MultiFieldPanel([FieldPanel("show_in_menus")], heading="Navigation"),
    ]
    seo_panels = seo_meta_panels + seo_menu_panels

    class Meta:
        abstract = True

@register_setting(icon="search")
class SEOSettings(BaseSiteSetting):
    site = models.OneToOneField(
        Site,
        on_delete=models.CASCADE,
        related_name="simple_seo_settings",
        editable=False,
    )

    default_description = models.TextField(
        blank=True,
        verbose_name="Default meta description",
        help_text="Used when a page does not provide its own meta description.",
    )
    default_social_image = models.ForeignKey(
        get_image_model_string(), blank=True, null=True,
        on_delete=models.SET_NULL, related_name="+",
        verbose_name="Default social image",
        help_text="Used when a page does not provide its own social preview image.",
    )

    panels = [FieldPanel("default_description"), FieldPanel("default_social_image")]

    class Meta:
        verbose_name = "SEO"
