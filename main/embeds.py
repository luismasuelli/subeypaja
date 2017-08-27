# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _


class EmbedEngine(object):

    key = ''
    name = ''

    def render(self, vid):
        raise NotImplementedError

    def description(self, vid):
        raise NotImplementedError


class RedTubeEngine(EmbedEngine):

    key = 'redtube'
    name = _('Redtube')

    def render(self, vid):
        """
        Inserta un video de RedTube en un iframe con cierto alto y ancho.

        :param id: El ID numérico del video.
        :param width: El ancho del iframe (el video se centrará).
        :param height: El alto del iframe (el video se centrará).
        :return: HTML del Embed

        RedTube sugiere predeterminadamente: 560x315, 640x360, 853x480, 1200x720.
        """

        return _("""
        <div class="alert alert-info" role="alert">
            <p>
                <strong>Tené en cuenta:</strong> Este video no está subido en nuestro sitio, sino en RedTube.
                Si querés ver el video original, podés hacer click <a href="https://www.redtube.com/%s">acá</a>.
            </p>
            <p>
                Si consideras que el video no es apropiado y pensás reportarlo, lo ideal es que el mismo video
                  sea reportado en RedTube. Normalmente, las normas de contenido inapropiado en un sitio adulto
                  son iguales en las diferentes jurisdicciones en donde el contenido adulto es legal.
            </p>
        </div>
        <iframe src="https://embed.redtube.com/?id=%s&bgcolor=000000"
                frameborder="0" width="%d" height="%d" scrolling="no"
                allowfullscreen=allowfullscreen />
        """) % (vid, vid, 640, 360)

    def description(self, vid):
        base = _('Redtube Embed - <a href="https://www.redtube.com/%s">see original video</a>')
        return mark_safe(base % vid)


class XVideosEngine(EmbedEngine):

    key = 'xvideos'
    name = _('XVideos')

    def render(self, vid):
        """
        Inserta un video de XVideos en un iframe con cierto alto y ancho.

        :param id: El ID numérico del video.
        :param width: El ancho del iframe (el video se centrará).
        :param height: El alto del iframe (el video se centrará).
        :return: HTML del Embed

        XVideos sugiere predeterminadamente 510x400.
        """

        return _("""
        <div class="alert alert-info" role="alert">
            <p>
                <strong>Tené en cuenta:</strong> Este video no está subido en nuestro sitio, sino en XVideos.
                Si querés ver el video original, podés hacer click <a href="https://www.xvideos.com/video%s/here">acá</a>.
            </p>
            <p>
                Si consideras que el video no es apropiado y pensás reportarlo, lo ideal es que el mismo video
                  sea reportado en RedTube. Normalmente, las normas de contenido inapropiado en un sitio adulto
                  son iguales en las diferentes jurisdicciones en donde el contenido adulto es legal.
            </p>
        </div>
        <iframe src="https://flashservice.xvideos.com/embedframe/%s"
                frameborder=0 width=%d height=%d scrolling=no
                allowfullscreen=allowfullscreen></iframe>
        """) % (vid, vid, 510, 400)

    def description(self, vid):
        base = _('XVideos Embed - <a href="https://www.xvideos.com/video%s/here">see original video</a>')
        return mark_safe(base % vid)


_EMBEDS_ENGINES = (RedTubeEngine(), XVideosEngine())
AVAILABLE_EMBEDS_CHOICES = tuple((engine.key, engine.name) for engine in _EMBEDS_ENGINES)
AVAILABLE_EMBEDS_ENGINES = {engine.key: engine for engine in _EMBEDS_ENGINES}
