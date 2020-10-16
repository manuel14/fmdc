import os

from django.contrib import admin
from django.conf import settings
import nested_admin

from web.models import Actividad, ActividadImage, Image, ImageAlbum, Song, Biografia, \
    Artista, EfemerideMes, Discoteca, Album, Video, AlbumSong, PagoActividad, RevistaImage, Revista

from .forms import AdminSongForm, ImagesRevistaForm
from .helpers import create_folder, copy_tmp_file_into_destination


def album_song_path(album):
    discoteca_name = album.discoteca.name.name
    path = f'archive/Discografias/{discoteca_name}/{album.name}'
    return path

class ImageInline(admin.StackedInline):
    model = Image
    extra = 1   
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class SongInline(admin.StackedInline):
    model = Song
    extra = 1
    exclude = ('link',)
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class AlbumSongInline(admin.StackedInline):
    model = AlbumSong
    form = AdminSongForm
    extra = 1
    exclude = ('link',)
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

class BiografiaAdmin(admin.ModelAdmin):
    inlines = [
        SongInline,
        ImageInline,
    ]
    search_fields = ('name__name',)
    raw_id_fields = ('name',)


admin.site.register(Biografia, BiografiaAdmin)


class EfemerideMesAdmin(admin.ModelAdmin):
    exclude = ('monthNumber', 'texto')


admin.site.register(EfemerideMes, EfemerideMesAdmin)


class ArtistaAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(Artista, ArtistaAdmin)


class ImageAInline(nested_admin.NestedStackedInline):
    model = ImageAlbum
    extra = 1
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class AlbumInline(nested_admin.NestedStackedInline):
    inlines = [
        ImageAInline,
    ]
    model = Album
    form = AdminSongForm
    extra = 3
    exclude = ('songString',)
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

class VideoInline(nested_admin.NestedStackedInline):
    model = Video
    extra = 1
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class ActividadImageInline(nested_admin.NestedStackedInline):
    model = ActividadImage
    extra = 1
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)


class DiscotecaAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        AlbumInline,
    ]
    search_fields = ('name__name',)
    raw_id_fields = ('name',)

admin.site.register(Discoteca, DiscotecaAdmin)


class ActividadAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        VideoInline,
        ActividadImageInline,
    ]
    exclude = ('text',)
    search_fields = ('title__title',)

class PagoActividadAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        VideoInline,
        ActividadImageInline,
    ]
    exclude = ('text',)
    search_fields = ('title__title',)

class RevistaImageInline(nested_admin.NestedStackedInline):
    model = RevistaImage
    exclude = ('name', 'link',)
    extra = 1
    form = ImagesRevistaForm
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)

class RevistaAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        RevistaImageInline,
    ]
    search_fields = ('numero',)


admin.site.register(Actividad, ActividadAdmin)
admin.site.register(PagoActividad, PagoActividadAdmin)
admin.site.register(Revista, RevistaAdmin)
