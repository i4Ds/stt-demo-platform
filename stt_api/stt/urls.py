from django.urls import path
from stt import views

urlpatterns = [
    path('transcribe/', views.transcribe),
    path('transcription/<str:pk>/rate/', views.rate),
    path('transcribe-long/', views.transcribe_long),
    path('long-status/<str:pk>', views.long_status),
    path('download-result/<str:pk>', views.download_result)
]
