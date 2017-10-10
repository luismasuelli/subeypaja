# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from grimoire.django.tracked.models import TrackedLive
from grimoire.django.tracked.models.polymorphic import TrackedLive as PolymorphicTrackedLive
from six import python_2_unicode_compatible
from main.embeds import AVAILABLE_EMBEDS_CHOICES, AVAILABLE_EMBEDS_ENGINES


class User(AbstractUser):

    def upload_requires_review(self):
        """
        En un futuro vamos a darle una implementación a este método para hacer que el nuevo
          contenido que sube este usuario requira revisión por parte de algún administrador.

        Se implementará un algoritmo que verificará faltas recientes del usuario o algun tipo
          de comportamiento que consideremos sospechoso por alguna razón.

        Por ahora, no lo implementamos.
        """

        return False

    def upload_is_disallowed(self):
        """
        En un futuro vamos a darle una implementación a este método para hacer que el usuario
          no pueda subir contenido alguno. Esto puede que sea temporal o definitivamente, pero
          si viene pensado como método, entonces lo más probable es que sea temporal y se
          trate automáticamente, más que algo como un ban o similar.
        """

        return False


@python_2_unicode_compatible
class Tag(TrackedLive):
    """
    Categorías (tags) de fotos, videos, enlaces.

    `special` nos sirve para categorizar el rubro del video (ej. si es humor, si es gore, ...).
    """

    name = models.CharField(max_length=100, null=False, blank=False)
    code = models.CharField(max_length=50, null=False, blank=False, unique=True)
    special = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return self.name


MF_STATUSES_ON_REVIEW = 'on_review'
MF_STATUSES_AVAILABLE = 'available'
MF_STATUSES_ON_HOLD = 'on_hold'
MF_STATUSES_BANNED = 'banned'
MF_STATUSES = (
    (MF_STATUSES_ON_REVIEW, _('On Review')),
    (MF_STATUSES_AVAILABLE, _('Available')),
    (MF_STATUSES_ON_HOLD, _('On Hold / Reported')),
    (MF_STATUSES_BANNED, _('Banned'))
)


class Media(PolymorphicTrackedLive):
    """
    Medios. Estos pueden ser enlaces, fotos, videos.

    Nos va a importar el usuario que lo subió y las categorías.

    Adicionalmente, un flujo de administración (la idea es que
      solamente se encuentre disponible desde el Admin) para
      los medias que tengan algún problema y sean disputados.
    Los estados son los siguientes:
      - On Review: El estado inicial para los usuarios de los
          que, por alguna razón, sospechamos. Va por criterio
          del administrador si lo permitimos, o no.
          Un media en este estado no será visible al público,
          sino solo al usuario.
      - Available: Disponible. El estado normal.
      - On Hold: Cuando un media file es reportado, y se sospecha
          que es inapropiado (infantil, no consentido, o
          denunciado por copyright) se pasa a este estado.
          Un media en este estado será visible solamente al
          usuario que lo subió.
      - Banned: Cuando la sospecha se toma por cierta, la foto
          es prohibida. Eventualmente el archivo será borrado
          en el storage, pero de seguro no será nuevamente
          accesible por el usuario.
    """

    # Ownership
    uploaded_by = models.ForeignKey(User, null=False, blank=False)

    # Info
    title = models.CharField(max_length=100, null=False, blank=False)
    details = models.TextField(max_length=1023, null=False, blank=True)
    tags = models.ManyToManyField(Tag, related_name='media')

    # Administration
    status = models.CharField(max_length=10, choices=MF_STATUSES, null=False, blank=False,
                              default=MF_STATUSES_AVAILABLE)
    inspection_notes = models.TextField(max_length=2**24, null=True, blank=True)

    def is_trusted(self):
        """
        Indica que el medio en cuestión es confiable. Esto implica que tendremos la
          garantía de que no hay porno infantil ni nada raro. Esto solamente es válido
          para medios externos o albums.

        En este sentido, no importa qué tanto desconfiemos de lo que sube un usuario,
          si esta función devuelve True, vamos a confiar en este contenido.
        """

        return True

    def save(self, *args, **kwargs):
        """
        Al guardar un nuevo registro, puede que nos vayamos por pedir revisión, o no.
          Esto si es que el mediafile es nuevo.
        """

        if self.uploaded_by and self.pk is None:
            self.status = MF_STATUSES_ON_REVIEW if self.uploaded_by.upload_requires_review() else MF_STATUSES_AVAILABLE
        return super(Media, self).save(*args, **kwargs)

    def description(self):
        return _('(Unknown media file type)')


class MediaHistory(TrackedLive):
    """
    Historia de cambios sobre un Media File, y motivos.
    """

    changed_by = models.ForeignKey(User, null=False, blank=False)
    media_file = models.ForeignKey(Media, null=False, blank=False)
    status = models.CharField(max_length=10, choices=MF_STATUSES, null=False, blank=False)
    details = models.TextField(max_length=2**15, null=True, blank=True)


class Image(Media):
    """
    Una foto, que será alojada por nosotros.
    Inicialmente el almacenamiento será en nuestro sitio web, pero con el tiempo nos pasaremos a Google Cloud Storage.
    """

    file = models.ImageField(upload_to='images', null=False, blank=False)

    def is_trusted(self):
        """
        Las imágenes no son medios de confianza automáticamente. Devolviendo False, nosotros hacemos que
          este contenido pueda ser demorado si desconfiamos del usuario.
        """

        return False

    def description(self):
        return mark_safe(_('Image - <a href="%s">see</a>') % self.file.url)


class Embed(Media):
    """
    Material embebido de otros sitios (como redtube y similares).
    """

    engine = models.CharField(max_length=20, choices=AVAILABLE_EMBEDS_CHOICES, null=False, blank=False)
    content = models.CharField(max_length=255, null=False, blank=False)

    def render(self):
        """
        Invokes the engine's render to get the appropriate HTML.
        :return: The appropriate HTML.
        """

        return AVAILABLE_EMBEDS_ENGINES[self.engine].render(self.content)

    def description(self):
        """
        Invokes the engine's description to get the appropriate description.
        :return: The appropriate description.
        """

        return AVAILABLE_EMBEDS_ENGINES[self.engine].description(self.content)


MAX_ALBUM_IMAGES = 12
class Album(Media):
    """
    Un album puede tener cualquier cosa en su interior, excepto otro album.
    """


class AlbumEntry(TrackedLive):
    """
    Entrada dentro de un album. Guarda elemento, posicion, y álbum.
    """

    sequence = models.PositiveSmallIntegerField(null=False)
    album = models.ForeignKey(Album, null=False, blank=False, related_name='entries')
    element = models.ForeignKey(Media, null=False, blank=False, related_name='entries')

    def clean(self):
        if isinstance(self.element, Album):
            raise ValidationError(_('An album cannot contain other albums'))

        if self.element.uploaded_by != self.album.uploaded_by:
            raise ValidationError(_('An album can only contain elements from the same owner'))

        if self.sequence >= MAX_ALBUM_IMAGES:
            raise ValidationError(_('An album element cannot be at position %d since it would go beyond '
                                    'the maximum') % self.sequence)

    class Meta:
        ordering = ('album', 'sequence')
        unique_together = (('album', 'sequence'), ('album', 'element'))
