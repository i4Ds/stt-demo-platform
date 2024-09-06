import uuid

from django.core.validators import FileExtensionValidator
from djongo import models

from stt.utils import UUIDFileName


class Rating(models.Model):
    rating = models.IntegerField()

    class Meta:
        abstract = True


class TranscribedClip(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    audio_file = models.FileField(
        upload_to=UUIDFileName('clips/%Y/%m/%d/'),
        validators=[
            FileExtensionValidator(allowed_extensions=['wav', 'wave', 'flac', 'mp3', 'm4a', 'mp4'])
        ]
    )
    transcription = models.TextField(blank=True)
    ratings = models.ArrayField(model_container=Rating, default=[])

    class Meta:
        db_table = 'transcribedclips'


class UploadFile(models.Model):
    file = models.FileField(
        upload_to=UUIDFileName('long/raw/%Y/%m/%d'),
        validators=[
            FileExtensionValidator(allowed_extensions=['wav', 'wave', 'flac', 'mp3', 'm4a', 'mp4', 'wma'])
        ]
    )
