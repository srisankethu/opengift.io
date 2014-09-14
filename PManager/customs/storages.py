__author__ = 'Gvammer'

from django.core.files.storage import FileSystemStorage
import os
from uuid import uuid4

def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(path, filename)
    return wrapper

class MyFileStorage(FileSystemStorage):

    # This method is actually defined in Storage
    def get_available_name(self, name):
        return name # simply returns the name passed
