import datetime
import os
import uuid

from django.utils.deconstruct import deconstructible


@deconstructible
class UUIDFileName(object):
    def __init__(self, path: str = ''):
        self.path = path

    def __call__(self, _, filename: str):
        dirname = datetime.datetime.now().strftime(str(self.path))
        extension = os.path.splitext(filename)[1]
        return os.path.join(dirname, f"{uuid.uuid4()}{extension}")

    def __eq__(self, other: 'UUIDFileName'):
        return self.path == other.path
