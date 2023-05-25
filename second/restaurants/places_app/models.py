from django.db import models
from . import config
from django.utils.translation import gettext_lazy as _


class Places(models.Model):
    name = models.TextField(_('name'), blank=False, null=False, max_length=config.CHARS_NAME)
    description = models.TextField(_('description'), blank=True, null=True, max_length=config.CHARS_DESC)
    map_points = models.TextField(_('map_points'), blank=False, null=False)
    map_scale = models.IntegerField(_('map_scale'), blank=False, null=False)

    class Meta:
        db_table = 'places'
