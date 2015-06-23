# -*- coding:utf-8 -*-
__author__ = 'Gvammer'
import os
import Image
from django.template import Library
from tracker import settings

register = Library()

@register.filter(name='thumbnail')
def thumbnail(file, size='200x200', resample=0):
    # defining the size
    x, y = [int(x) for x in size.split('x')]
    # defining the filename and the miniature filename
    basename, format = file.rsplit('.', 1)
#    print basename
    miniature = basename + '_' + size + '.' +  format
    miniature = miniature.replace('media/', 'media/thumbnails/')
    miniature_filename = os.path.join(settings.MEDIA_ROOT, miniature)
    miniature_url = str(miniature)
    miniature_dir = miniature_filename.split('/')
    del(miniature_dir[-1])
    miniature_dir = '/'.join(miniature_dir)

    # if the image wasn't already resized, resize it
    if not os.path.exists(miniature_filename):
#        print '>>> debug: resizing the image to the format %s!' % size
        filename = os.path.join(settings.MEDIA_ROOT, file)

        if os.path.isfile(filename):
            try:
                if not os.path.exists(miniature_dir):
                    os.makedirs(miniature_dir)

                image = Image.open(filename)
                image.thumbnail([x, y], resample) # generate a 200x200 thumbnail
                image.save(miniature_filename, image.format)
            except IOError:
                return file
    return miniature_url

@register.filter(name='protected')
def protected(url):
    if url.startswith('/'):
        url = url[1:]
    return os.path.join('/protected', str(url))
