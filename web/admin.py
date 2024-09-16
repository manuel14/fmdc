import os

from django.contrib import admin
from django.conf import settings
import nested_admin

from web.models import Actividad, ActividadImage, ActividadFile, ActividadSong, Image, ImageAlbum, Song, Biografia, \
    Artista, EfemerideMes, Discoteca, Album, Video, PagoActividad, Revista, RevistaImage, Editorial

from .forms import AdminSongForm
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

class ActividadFileInline(nested_admin.NestedStackedInline):
    model = ActividadFile
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
        ActividadFileInline
    ]
    exclude = ('text',)
    search_fields = ('name',)

    def save_model(self, request, obj, form, change):
        obj.save()
        song_names = ActividadSong.objects.values_list("name", flat=True)
        for song in request.FILES.getlist('canciones_multiple'):
            song_name = song.name.split(".")[0]
            if song_name in song_names:
                continue
            song = ActividadSong.objects.create(
                act=obj,
                name=song_name,
                link=song
            )


class PagoActividadAdmin(nested_admin.NestedModelAdmin):
    inlines = [
        VideoInline,
        ActividadImageInline,
    ]
    exclude = ('text',)
    search_fields = ('title__title',)

class RevistaAdmin(nested_admin.NestedModelAdmin):
    exclude = ()
    search_fields = ()
    ordering = ('fecha',)

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.imagenes_revista.all().delete()
        for image_file in request.FILES.getlist('images_multiple'):
            imagen = RevistaImage(
                revista=obj,
                link=image_file
            )
            imagen.save()

class EditorialAdmin(admin.ModelAdmin):
    exclude = ()
    ordering = ('title',)

    def save_model(self, request, obj, form, change):
        obj.save()
        obj.archivos_editorial.all().delete()
        for arch in request.FILES.getlist('editorial_canciones_multiple'):
            file_name = arch.name.split(".")[0]
            EditorialFile.objects.create(
                editorial=obj,
                name=file_name,
                link=arch
            )


admin.site.register(Actividad, ActividadAdmin)
admin.site.register(PagoActividad, PagoActividadAdmin)
admin.site.register(Revista, RevistaAdmin)
admin.site.register(Editorial, EditorialAdmin)