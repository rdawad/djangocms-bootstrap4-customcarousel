from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from .models import Testing


# imports for custom carousel 
# https://github.com/django-cms/djangocms-bootstrap4/blob/master/djangocms_bootstrap4/contrib/bootstrap4_carousel/cms_plugins.py

from django.utils.translation import gettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from djangocms_link.cms_plugins import LinkPlugin

from djangocms_bootstrap4.helpers import concat_classes, get_plugin_template

from .constants import CAROUSEL_DEFAULT_SIZE, CAROUSEL_TEMPLATE_CHOICES
from .models import CustomBootstrap4Carousel, CustomBootstrap4CarouselSlide


@plugin_pool.register_plugin
class TestingPlugin(CMSPluginBase):
    model = Testing
    name = ("testing plugin")
    render_template = "test.html"
    allow_children = True

    def render(self,context,instance,placeholder):
        context = super().render(context,instance,placeholder)
        return context
    
@plugin_pool.register_plugin
class CustomBootstrap4CarouselPlugin(CMSPluginBase):
    """
    Components > "Carousel" Plugin
    https://getbootstrap.com/docs/4.0/components/carousel/
    """
    model = CustomBootstrap4Carousel
    name = _('Custom Carousel')
    module = _('Bootstrap 4')
    render_template = "carousel.html"
    allow_children = True
    child_classes = ['CustomBootstrap4CarouselSlidePlugin']

    fieldsets = [
        (None, {
            'fields': (
                ('carousel_aspect_ratio', 'carousel_interval'),
                ('carousel_controls', 'carousel_indicators'),
                ('carousel_keyboard', 'carousel_wrap'),
                ('carousel_ride', 'carousel_pause'),
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'template',
                'tag_type',
                'attributes',
            )
        }),
    ]

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance, 'carousel', 'carousel', CAROUSEL_TEMPLATE_CHOICES
        )
        # return "carousel.html"

    def render(self, context, instance, placeholder):
        link_classes = ['carousel', 'slide']

        classes = concat_classes(link_classes + [
            instance.attributes.get('class'),
        ])
        instance.attributes['class'] = classes

        return super().render(
            context, instance, placeholder
        )


@plugin_pool.register_plugin
class CustomBootstrap4CarouselSlidePlugin(LinkPlugin):
    """
    Components > "Carousel Slide" Plugin
    https://getbootstrap.com/docs/4.0/components/carousel/
    """
    model = CustomBootstrap4CarouselSlide
    name = _('Custom Carouselslide')
    module = _('Bootstrap 4')
    render_template = "slide.html"
    allow_children = True
    parent_classes = ['CustomBootstrap4CarouselPlugin']

    fieldsets = [
        (None, {
            'fields': (
                'carousel_image',
                'carousel_content',
            )
        }),
        (_('Link settings'), {
            'classes': ('collapse',),
            'fields': (
                ('external_link', 'internal_link'),
                ('mailto', 'phone'),
                ('anchor', 'target'),
            )
        }),
        (_('Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                'tag_type',
                'attributes',
            )
        }),
    ]

    def render(self, context, instance, placeholder):
        parent = instance.parent.get_plugin_instance()[0]
        width = float(context.get('width') or CAROUSEL_DEFAULT_SIZE[0])
        height = float(context.get('height') or CAROUSEL_DEFAULT_SIZE[1])

        if parent.carousel_aspect_ratio:
            aspect_width, aspect_height = tuple(
                int(i) for i in parent.carousel_aspect_ratio.split('x')
            )
            height = width * aspect_height / aspect_width

        link_classes = ['carousel-item']
        if instance.position == 0:
            link_classes.append('active')
        classes = concat_classes(link_classes + [
            instance.attributes.get('class'),
        ])
        instance.attributes['class'] = classes

        context['instance'] = instance
        context['link'] = instance.get_link()
        context['options'] = {
            'crop': 10,
            'size': (width, height),
            'upscale': True
        }
        return context

    def get_render_template(self, context, instance, placeholder):
        return get_plugin_template(
            instance.parent.get_plugin_instance()[0],
            'carousel',
            'slide',
            CAROUSEL_TEMPLATE_CHOICES,
        )
        # return "slide.html"

