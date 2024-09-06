from rest_framework import serializers

from stt.models import TranscribedClip, UploadFile


class TranscribedClipSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscribedClip
        fields = ['id', 'created', 'audio_file', 'transcription', 'ratings']


class UploadFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadFile
        fields = ['file']