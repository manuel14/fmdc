# -*- coding: utf-8 -*-
import json
import random

from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.views import generic
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, F
from django.core.paginator import Paginator
from django.conf import settings


from .models import (
    Actividad,
    Artista,
    Biografia,
    Discoteca,
    Editorial,
    Efemeride,
    EfemerideMes,
    Revista
)
from web.folder_service import FolderService

folder_service = FolderService()


def index(request):
    return render(request, 'web/index.html')


def imgLaterales(request):
    if not request.is_ajax():
        raise Http404('No se puede acceder a esta url.')
    images = folder_service.get_side_images(path='Laterales')
    return HttpResponse(json.dumps(random.sample(images, 6), cls=DjangoJSONEncoder, ensure_ascii=False))


class GaleriaView(generic.ListView):
    template_name = 'web/galerias.html'
    
    def get_queryset(self):
        photo_galleries = folder_service.get_folder_names_from_path(path="/archive/Galeria/Fotos")
        video_galleries = folder_service.get_folder_names_from_path(path="/archive/Galeria/Videos")
        return {
            'images': photo_galleries,
            'videos': video_galleries
        }


class GaleriaCView(generic.DetailView):
    template_name = 'web/galeriaWithLetters.html'

    def get_object(self):
        obj = {}
        folder_letter = self.kwargs.get('path', None)
        if folder_letter is None:
            return obj
        path = '/archive/Galeria/Fotos/Fotos Chamameseros/' + folder_letter
        music_sheet_images = folder_service.get_files_from_folder(path=path)
        obj['images'] = music_sheet_images[0:4]
        obj['lazyImages'] = music_sheet_images[4:]
        return obj


class GaleriaDetailView(generic.DetailView):
    template_name = 'web/galeria.html'

    def get_object(self):
        obj = {}
        obj = {}
        folder_letter = self.kwargs['path']
        if folder_letter is None:
            return obj
        path = '/archive/Galeria/Fotos/' + folder_letter
        gallery_images = folder_service.get_files_from_folder(path=path)
        obj['images'] = gallery_images[0:4]
        obj['lazyImages'] = gallery_images[4:]
        obj['name'] = folder_letter.replace('/', '')
        return obj


class VideoView(generic.DetailView):
    template_name = 'web/videoWithLetters.html'

    def get_object(self):
        obj = {}
        folder_letter = self.kwargs.get('path', None)
        if folder_letter is None:
            return obj
        path = '/archive/Galeria/Videos/' + folder_letter.lower()
        videos = folder_service.get_files_from_folder(path=path)
        obj['videos'] = videos
        return obj


class BiografiaView(generic.ListView):
    template_name = 'web/biografias.html'

    def get_queryset(self):
        filtro = self.kwargs.get('filtro', None)
        if filtro is None:
            return Biografia.objects.all().order_by('name__name')
        values = filtro[:-1].split()
        queries = [Q(name__name__icontains=value) for value in values]
        query = queries.pop()
        for item in queries:
            query &= item
        return Biografia.objects.filter(query).order_by('name__name')


class BiografiaDetailView(generic.DetailView):
    model = Biografia
    template_name = 'web/biografia.html'


class BusquedaView(generic.ListView):
    template_name = 'web/busqueda.html'

    def get_queryset(self):
        lookup_filter = self.kwargs.get('filtro', None)
        values = lookup_filter.split()
        queries = [Q(name__icontains=value) for value in values]
        query = queries.pop()
        for item in queries:
            query &= item
        return Artista.objects.filter(query).order_by('name')


class DiscotecaView(generic.ListView):
    template_name = 'web/discotecas.html'

    def get_queryset(self):
        lookup_filter = self.kwargs.get('filtro', None)
        if lookup_filter is None:
            return Discoteca.objects.all().order_by('name__name')
        filter_without_backslash = lookup_filter[:-1]
        discotecas = Discoteca.objects.filter(Q(
            name__name__icontains=filter_without_backslash) | 
            Q(albumes__name__icontains=filter_without_backslash)).distinct().order_by('name__name')
        return discotecas

def discoteca(request, pk):
    discoteca = Discoteca.objects.get(pk=pk)
    albumes = discoteca.albumes.order_by(F('year').asc(nulls_last=True))
    return render(request, 'web/discoteca.html',
                  {"discoteca": discoteca, "albumes":albumes})



class PartiturasCView(generic.DetailView):
    template_name = 'web/partituras.html'

    def get_object(self):
        obj = {}
        folder_letter = self.kwargs.get('path', None)
        if folder_letter is None:
            return obj
        path = '/archive/Material/Partituras/' + folder_letter.lower()
        music_sheet_images = folder_service.get_files_from_folder(path=path)
        obj['images'] = music_sheet_images
        return obj


class LetrasCView(generic.DetailView):
    template_name = 'web/letras.html'

    def get_object(self):
        obj = {}
        folder_letter = self.kwargs.get('path', None)
        if folder_letter is None:
            return obj
        path = '/archive/Material/Letras/' + folder_letter.lower()
        lyrics = folder_service.get_files_from_folder(path=path)
        obj['lyrics'] = lyrics
        return obj

class LetrasView(generic.TemplateView):
    template_name = 'web/letras.html'


class ActividadView(generic.ListView):
    template_name = 'web/actividadesLista.html'

    def get_queryset(self):
        lookup_filter = self.kwargs.get('filtro', None)
        if lookup_filter is None:
            return Actividad.objects.exclude(tipo=Actividad.PAGO_ACTIVIDAD).order_by('name')
        filter_without_backslash = lookup_filter[:-1].strip()
        return Actividad.objects.filter(
            name__icontains=filter_without_backslash).exclude(tipo=Actividad.PAGO_ACTIVIDAD).order_by('name')


class ActividadDetailView(generic.DetailView):
    model = Actividad
    template_name = 'web/actividad.html'


def consejoAdm(request):
    return render(request, 'web/quienesSomos.html')

def consejoCon(request):
    return render(request, 'web/consejoCon.html')

def miembros(request):
    return render(request, 'web/miembros.html')

def objetivos(request):
    return render(request, 'web/objetivos.html')


def efemerides(request):
    todayDay = datetime.today().day
    todayMonth = datetime.today().month
    efemerides = Efemeride.objects.filter(date__day=todayDay, date__month=todayMonth)
    efemeridesPorMes = {}
    for efem in EfemerideMes.objects.all():
        efemeridesPorMes[efem.month] = {'efemerides': list(efem.efemeride_set.all().values_list('date', 'event'))}
    allEfemerides = json.dumps(efemeridesPorMes, cls=DjangoJSONEncoder, ensure_ascii=False)
    return render(request, 'web/efemeride.html', {'efemerides': efemerides, 'allEfemerides': allEfemerides})


def benefactores(request):
    return render(request, 'web/benefactores.html')


def material(request):
    return render(request, 'web/material.html')


def partituras(request):
    return render(request, 'web/partituras.html')


def radio(request):
    path = "/radio"
    contents = folder_service.get_folders_with_their_contents(path)
    return render(request, 'web/radio.html', {"contents": contents})


def revistas(request):
    revistas_objs = Revista.objects.exclude(
        imagenes_revista__isnull=True).order_by('fecha')

    paginator = Paginator(revistas_objs, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'revistas': page_obj}

    return render(request, 'web/revistas.html', context)


def revista(request, pk):
    revista = Revista.objects.get(pk=pk)
    revista_imagenes = sorted(
        revista.imagenes_revista.all(), key=lambda r: r.link.name)
    return render(
        request,
        'web/revista.html',
        {'revista': revista, 'imagenes': revista_imagenes,
            'total': len(revista_imagenes)}
    )


def editoriales(request):
    editoriales_list = Editorial.objects.all()
    return render(
        request,
        "web/editoriales.html",
        {'editoriales': editoriales_list}
    )

def editorial(request, pk=None):
    if pk is None:
        return render(request, 'web/404.html')
    editorial = Editorial.objects.get(pk=pk)
    return render(
        request,
        "web/editorial.html",
        {'editorial': editorial}
    )


def mapa(request):
    # video_url = f"{settings.MEDIA_URL}/files/corrientes_mapa.MP4"
    video_url = f"{settings.MEDIA_URL}mapa/videos/corrientes_mapa.MP4"
    alvear = f"{settings.MEDIA_URL}mapa/videos/ALVEAR.mp4"
    paso = f"{settings.MEDIA_URL}mapa/videos/PASODELOSLIBRES.mp4"
    videos_map = {"corrientes": video_url,
                  "pasodeloslibres": paso, "alvear": alvear}
    departments = {
        "alvear": "Alvear",
        "bellavista": "Bella Vista",
        "berondeastrada": "Berón de Astrada",
        "caacati": "Caá Catí",
        "corrientes": "Corrientes",
        "concepcion": "Concepción",
        "curuzucuatia": "Curuzú Cuatiá",
        "empedrado": "Empedrado",
        "esquina": "Esquina",
        "goya": "Goya",
        "itati": "Itatí",
        "ituzaingo": "Ituzaingó",
        "lacruz": "La Cruz",
        # "lavalle": "Lavalle",
        "pasodeloslibres": "Paso de los Libres",
        "mburucuya": "Mburucuyá",
        "sanmartin": "San Martín",
        "montecaseros": "Monte Caseros",
        "sanroque": "San Roque",
        "saladas": "Saladas",
        "sancosme": "San Cosme",
        "sanluisdelpalmar": "San Luis del Palmar",
        "sanmiguel": "San Miguel",
        "santotome": "Santo Tomé",
        "santalucia": "Santa Lucía",
        "sauce": "Sauce",
    }
    return render(request, "web/mapa.html", {"departments": departments,
                                             "videoUrls": json.dumps(videos_map)})


def error404(request, exception=None):
    return render(request, 'web/404.html')


def error500(request, exception=None):
    return render(request, 'web/500.html')
