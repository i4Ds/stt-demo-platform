import logging

import requests
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import renderers
from django.http import FileResponse
from io import BytesIO

from stt.models import TranscribedClip, UploadFile
from stt.serializers import TranscribedClipSerializer, UploadFileSerializer

logger = logging.getLogger(__name__)


@api_view(['POST'])
def transcribe(request: Request):
    serializer = TranscribedClipSerializer(data=request.data)
    if serializer.is_valid():
        transcribed_clip: TranscribedClip = serializer.save()

        url = 'http://api:5000/transcribe'
        files = {'file': open(transcribed_clip.audio_file.path, 'rb')}
        try:
            response = requests.post(url=url, files=files)
            transcribed_clip.transcription = response.text
        except requests.exceptions.RequestException:
            logger.exception('Error during transcription request')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        try:
            transcribed_clip.save(update_fields=['transcription'])
        except Exception:
            logger.exception('Error while saving transcription')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def rate(request: Request, pk: str):
    try:
        transcribed_clip = TranscribedClip.objects.get(pk=pk)
    except TranscribedClip.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = JSONParser().parse(request)
    serializer = TranscribedClipSerializer(
        transcribed_clip,
        data={'ratings': [data]},
        partial=True
    )
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def transcribe_long(request: Request):
    serializer = UploadFileSerializer(data=request.data)
    
    if serializer.is_valid():
        uploaded_file: UploadFile = serializer.save()
        save_path = uploaded_file.file.path

        url_long_transcription = 'http://long-api:5050/transcribe-long'

        try:
            response = requests.post(url=url_long_transcription, data={'file_path': save_path, 'speakers': int(request.data.get("speakers", 0))})
        except requests.exceptions.RequestException:
            logger.exception('Error')
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(response.json(), status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def long_status(request: Request, pk: str):
    url_status = f'http://long-api:5050/status/{pk}'
    response = requests.get(url=url_status)
    return Response(response.json(), status=status.HTTP_200_OK)

class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data

@api_view(['GET'])
@renderer_classes([PassthroughRenderer])
def download_result(request: Request, pk: str):
    type = request.GET.get('type')
    if type == 'csv':
        content_type='text/csv; charset=utf-8'
    elif type == 'txt':
        content_type='text/plain; charset=utf-8'
    elif type == 'json':
        content_type='application/json; charset=utf-8'
    elif type == 'srt':
        content_type='text/plain; charset=utf-8'
    else:
        return Response('Unsupported type', status=status.HTTP_400_BAD_REQUEST)

    file_name = f'export_{pk}.{type}'

    url_generate = f'http://long-api:5050/generate/{pk}'
    r = requests.get(url=url_generate, data={'type': type})
    data = r.json()

    file_content = data['content']

    content_bytes = bytes(file_content, 'utf-8')
    stream = BytesIO(content_bytes)
    response = FileResponse(stream, content_type, as_attachment=True, filename=file_name)

    return response
