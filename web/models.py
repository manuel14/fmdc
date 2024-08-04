# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date
import re

from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from tinymce import models as tinymce_models


def album_song_path(instance, filename):
    return f'archive/Discografias/{instance.album.artista.name}/{instance.album.name}/{filename}'

def get_tapa_editorial_upload_path(instance, filename):
    return f"editoriales/{instance.title}/{filename}"

class Artista(models.Model):
    """
    Represents an artist
    """
    name = models.CharField('Nombre', max_length=70)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = 'Artista'
        verbose_name_plural = 'Artistas'


class Biografia(models.Model):
    """
    Represents an artist biography
    """
    name = models.OneToOneField(
        Artista, on_delete=models.CASCADE, null=True, blank=True)
    text = tinymce_models.HTMLField()

    def __str__(self):
        return self.name.name

    def save(self, *args, **kwargs):
        self.text = self.text.replace("color:", "")
        self.text = re.sub(r"background:\s*[^;]+;", "", self.text, flags=re.IGNORECASE)
        super(Biografia, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name']
        verbose_name = 'Biografia'
        verbose_name_plural = 'Biografias'


class Song(models.Model):
    """
    Represents a song related to a biography
    """
    songs = models.ForeignKey(Biografia, default=None,
                              on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField('Nombre', max_length=70)
    extraInfo = models.TextField('Informacion extra', blank=True)
    link = models.CharField('Enlace', max_length=300)
    link_org = models.CharField('Enlace', max_length=300)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        pattern = re.compile(r'^\[audio:([\w\/\.]+)\]$', re.UNICODE)
        url = settings.MEDIA_URL + 'archive/Biografias/' + \
            re.match(pattern, self.link_org).group(1)
        self.link = r'<audio controls controlsList="nodownload"><source src="' + url + \
            '" type="audio/mpeg">Su explorador es antiguo. Actualicelo para reproducir audios.</audio>'
        super(Song, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cancion'
        verbose_name_plural = 'Canciones'


class Image(models.Model):
    """
    Represents an Image
    """
    bio = models.ForeignKey(Biografia, default=None,
                            on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField('Imagen', upload_to='images/', default='')
    description = models.CharField('Descripcion', max_length=200, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'


class EfemerideMes(models.Model):
    """
    Represents a monthly important event
    """
    month = models.CharField('Mes', max_length=10)
    monthNumber = models.IntegerField()
    texto = models.TextField('Efemerides')
    texto_org = models.TextField('Efemerides')

    def __str__(self):
        return self.month

    def monthFromString(self, x):
        return {
            'Enero': 1,
            'Febrero': 2,
            'Marzo': 3,
            'Abril': 4,
            'Mayo': 5,
            'Junio': 6,
            'Julio': 7,
            'Agosto': 8,
            'Septiembre': 9,
            'Octubre': 10,
            'Noviembre': 11,
            'Diciembre': 12
        }.get(x)

    class Meta:
        verbose_name = 'Efemeride por mes'
        verbose_name_plural = 'Efemerides por mes'

    def save(self, *args, **kwargs):
        self.monthNumber = self.monthFromString(self.month)
        self.texto = self.texto_org.replace(
            '\n', '').replace('\r', '').replace('"', '&quot;')
        super(EfemerideMes, self).save(*args, **kwargs)
        if (self.efemeride_set.all() != []):
            self.efemeride_set.all().delete()
        pattern = re.compile(r"""dia:([0-9]+) *\[(.+?)\]""", flags=re.UNICODE)
        pattern2 = re.compile(r"""([0-9]+) *\| *([\W\D .]+)""",
                              flags=re.UNICODE)
        for (dia, efemeride) in re.findall(pattern, self.texto):
            for (anio, efe) in re.findall(pattern2, efemeride):
                efem = Efemeride()
                efem.date = date(int(anio), self.monthNumber, int(dia))
                efem.event = efe
                efem.mes = self
                efem.save()


class Efemeride(models.Model):
    """
    Represents an important event
    """
    mes = models.ForeignKey(EfemerideMes, on_delete=models.CASCADE)
    date = models.DateField('Fecha')
    event = models.CharField('Efemeride', max_length=300)

    def __str__(self):
        return self.date.strftime('Efemeride del %d, %b')

    class Meta:
        verbose_name = 'Efemeride'
        verbose_name_plural = 'Efemerides'


class Discoteca(models.Model):
    """
    Represents a collection of albums for an artist
    """
    name = models.OneToOneField(
        Artista,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    def __str__(self):
        return "Discoteca de " + self.name.name


class Album(models.Model):
    """
    Represents an album
    """
    discoteca = models.ForeignKey(
        Discoteca,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='albumes'
    )
    name = models.CharField('Nombre', max_length=100)
    tapa = models.ImageField(
        'Tapa', upload_to='images/', default='', blank=True)
    lamina = models.ImageField(
        'Lamina', upload_to='images/', default='', blank=True)
    year = models.IntegerField('Año (Periodo inicio)', null=True, blank=True)
    yearEnd = models.IntegerField('Año (Periodo final)', null=True, blank=True)
    songString = models.TextField('Listado de canciones', blank=True)
    songString_org = models.TextField('Listado de canciones', blank=True)

    def formatHelper(self, matchobj):
        url = settings.MEDIA_URL + 'archive/Discografias/' + matchobj.group(1)
        return r'<audio controls preload="none"><source src="'+url+'" type="audio/mpeg">Su explorador es antiguo\. Actualicelo para reproducir audios\.</audio>'

    def save(self, *args, **kwargs):
        p = re.compile(r'\[audio:([\w\/\.]+)\]', re.UNICODE)
        self.songString = re.sub(p, self.formatHelper, self.songString_org)
        self.songString = self.songString.replace('\n', r'<br>')
        super(Album, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Album'
        verbose_name_plural = 'Albumes'

    def __str__(self):
        return self.name

    @property
    def template_title(self):
        """
        Returns the title for the album for the template
        """
        if self.year and self.yearEnd:
            return f"{self.name} {self.year}-{self.yearEnd}"
        elif self.year:
            return f"{self.name} {self.year}"
        else:
            return self.name


class ImageAlbum(models.Model):
    """
    Represents an image for an album
    """
    alb = models.ForeignKey(Album, default=None, on_delete=models.CASCADE)
    image = models.ImageField('Imagen', upload_to='images/', default='')
    description = models.CharField('Descripcion', max_length=200, blank=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'


class Actividad(models.Model):
    """
    Represents an event
    """
    name = models.CharField('Nombre', max_length=100)
    description = tinymce_models.HTMLField()
    fecha = models.DateField('Fecha', default=date.today)
    ACTIVIDAD = "A"
    PAGO_ACTIVIDAD = "P"
    tipos = (
        (ACTIVIDAD, "Actividad"),
        (PAGO_ACTIVIDAD, "Pago Actividad")
    )
    tipo = models.TextField(choices=tipos, default="A")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Actividad'
        verbose_name_plural = 'Actividades'


class Video(models.Model):
    """
    Represents a video
    """
    name = models.CharField(max_length=100)
    videos = models.ForeignKey(Actividad, default=None, on_delete=models.CASCADE,
                               null=True, blank=True)
    link = models.FileField('Video', upload_to='videos/',
                            validators=[FileExtensionValidator(
                                allowed_extensions=['mp4'])],
                            default='')

    def __str__(self):
        return self.name


class ActividadImage(models.Model):
    """
    Represents an event's image
    """
    name = models.CharField(max_length=100)
    act = models.ForeignKey(Actividad, default=None, on_delete=models.CASCADE,
                            null=True, blank=True)
    link = models.ImageField('Imagen', upload_to='images/', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'

class ActividadFile(models.Model):
    """
    Represents an event's image
    """
    name = models.CharField(max_length=100)
    act = models.ForeignKey(Actividad, default=None, on_delete=models.CASCADE,
                            null=True, blank=True)
    link = models.FileField('Archivo', upload_to='files/', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Archivo'
        verbose_name_plural = 'Archivos'

class ActividadSong(models.Model):
    """
    Represents an event's image
    """
    name = models.CharField(max_length=100)
    act = models.ForeignKey(Actividad, default=None, on_delete=models.CASCADE,
                            null=True, blank=True, related_name="canciones")
    link = models.FileField('CancionActividad', upload_to='files/', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Cancion activdad'
        verbose_name_plural = 'Canciones de actividad'

class PagoActividad(Actividad):
    tipo = Actividad.PAGO_ACTIVIDAD

    class Meta:
        verbose_name = 'Actividad del pago'
        verbose_name_plural = 'Actividades del pago'


class Revista(models.Model):
    class Meta:
        verbose_name = 'Revista'
        verbose_name_plural = 'Revistas'

    nombre = models.TextField()
    fecha = models.DateField('Fecha', auto_now=False, auto_now_add=False)
    tapa = models.ImageField('Tapa revista', upload_to='images/', default='')

    def __str__(self):
        return self.nombre

class RevistaImage(models.Model):
    """
    Represents an event's image
    """
    revista = models.ForeignKey(Revista, default=None, on_delete=models.CASCADE,
                            null=True, blank=True, related_name='imagenes_revista')
    link = models.ImageField('Revista Imagen', upload_to='images/', default='')

    def __str__(self):
        return self.revista.nombre

    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'

class Editorial(models.Model):
    """
    Represents an editorial object
    """
    title = models.CharField(max_length=200)
    tapa = models.ImageField('Tapa editorial', upload_to=get_tapa_editorial_upload_path)
    link = models.FileField('Editorial', upload_to=get_tapa_editorial_upload_path,
                            validators=[FileExtensionValidator(
                                allowed_extensions=['pdf'])],)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Editorial'
        verbose_name_plural = 'Editoriales'