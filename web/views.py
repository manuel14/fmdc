# -*- coding: utf-8 -*-
import os
import json
import random

from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.views import generic
from datetime import datetime
from django.core.mail import EmailMessage
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Q, F
from django.conf import settings

from .forms import ContactForm
from .models import (
    Actividad,
    Artista,
    Biografia,
    Discoteca,
    Efemeride,
    EfemerideMes,
    Revista
)
from web.constants import IMAGE_EXTENSION_PATTERN, MP4_EXTENSION_PATTERN, PDF_EXTENSION_PATTERN
from web.helpers import get_files_from_folder_path
from web.helpers import safe_unicode_str


def index(request):
    return render(request, 'web/index.html')


def imgLaterales(request):
    if not request.is_ajax():
        raise Http404('No se puede acceder a esta url.')
    urls = [os.path.join(settings.MEDIA_URL + 'Laterales/', safe_unicode_str(fn)) for fn in os.listdir(settings.MEDIA_ROOT+'Laterales/')]
    return HttpResponse(json.dumps(random.sample(urls, 6), cls=DjangoJSONEncoder, ensure_ascii=False))


class GaleriaView(generic.ListView):
    template_name = 'web/galerias.html'
    
    def get_queryset(self):
        images = [folder for folder in os.listdir(settings.MEDIA_ROOT+'/archive/Galeria/Fotos')
                if os.listdir(settings.MEDIA_ROOT+'/archive/Galeria/Fotos/'+folder)
        ]
        videos = [folder for folder in os.listdir(settings.MEDIA_ROOT+'/archive/Galeria/Videos')
                if os.listdir(settings.MEDIA_ROOT+'/archive/Galeria/Videos/'+folder)
        ]
        return {
            'images': images,
            'videos': videos
        }


class GaleriaCView(generic.DetailView):
    template_name = 'web/galeriaWithLetters.html'

    def get_object(self):
        obj = {}
        folder_letter = self.kwargs['path']
        if folder_letter is None:
            return obj
        path = '/archive/Galeria/Fotos/Fotos Chamameseros/' + folder_letter
        music_sheet_images = get_files_from_folder_path(path=path, pattern=IMAGE_EXTENSION_PATTERN)
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
        gallery_images = get_files_from_folder_path(path=path, pattern=IMAGE_EXTENSION_PATTERN)
        obj['images'] = gallery_images[0:4]
        obj['lazyImages'] = gallery_images[4:]
        obj['name'] = folder_letter.replace('/', '')
        return obj


class VideoView(generic.DetailView):
    template_name = 'web/videoWithLetters.html'

    def get_object(self):
        obj = {}
        folder_letter = self.kwargs['path']
        if folder_letter is None:
            return obj
        path = '/archive/Galeria/Videos/' + folder_letter
        videos = get_files_from_folder_path(path=path, pattern=MP4_EXTENSION_PATTERN)
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
        folder_letter = self.kwargs['path']
        if folder_letter is None:
            return obj
        path = '/archive/Material/Partituras/' + folder_letter
        music_sheet_images = get_files_from_folder_path(path=path, pattern=IMAGE_EXTENSION_PATTERN)
        obj['images'] = music_sheet_images
        return obj


class LetrasCView(generic.DetailView):
    template_name = 'web/letras.html'

    def get_object(self):
        obj = {}
        folder_letter = self.kwargs['path']
        if folder_letter is None:
            return obj
        path = '/archive/Material/Letras/' + folder_letter
        lyrics = get_files_from_folder_path(path=path, pattern=PDF_EXTENSION_PATTERN)
        obj['lyrics'] = lyrics
        return obj


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


def cancionero(request):
    return render(request, 'web/cancionero.html')


def radio(request):
    contents = {}
    radio_contents_path = f"{settings.MEDIA_ROOT}/radio"
    for folder in os.listdir(radio_contents_path):
        # We need to add this hack to avoid UnicodeEncodeError with surrogates
        encoded_folder = safe_unicode_str(folder)
        folder_path = os.path.join(radio_contents_path, encoded_folder)
        for file in os.listdir(folder_path):
            encoded_file = safe_unicode_str(file)
            if os.path.isfile(os.path.join(folder_path, file)):
                relative_path = os.path.join(settings.MEDIA_URL, "radio", encoded_folder)
                file_url = f"{relative_path}/{encoded_file}"
                try:
                    contents[encoded_folder].append({
                        "name": encoded_file,
                        "url": file_url 
                    })
                except KeyError:
                    contents[encoded_folder] = [ {"name": encoded_file, "url": file_url} ]
    for folder_name, folder_content in contents.items():
        contents[folder_name] = sorted(folder_content, key=lambda item: item["name"])
    contents = {k:v for k,v in sorted(contents.items(), key=lambda item: item[0])}
    return render(request, 'web/radio.html', {"contents": contents})

def revistas(request):
    revistas = Revista.objects.exclude(imagenes_revista__isnull=True).order_by('fecha')
    context = {'revistas': revistas}
    return render(request, 'web/revistas.html', context)

def revista(request, pk):
    revista = Revista.objects.get(pk=pk)
    revista_imagenes = sorted(revista.imagenes_revista.all(), key=lambda r: r.link.name)
    return render(
        request,
        'web/revista.html',
        {'revista': revista, 'imagenes': revista_imagenes, 'total': len(revista_imagenes)}
    )

def error404(request, exception=None):
    return render(request, 'web/404.html')


def error500(request, exception=None):
    return render(request, 'web/500.html')