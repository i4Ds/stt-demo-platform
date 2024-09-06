import numpy as np
import pysubs2
import torch
import os
import whisperx
import torchaudio
from whisperx.alignment import DEFAULT_ALIGN_MODELS_HF
from moviepy.editor import VideoFileClip

DEFAULT_ALIGN_MODELS_HF["de"] = "scasutt/wav2vec2-large-xlsr-52_Swiss_German"


def align_with_whisperx(list_of_dict, audio, device, language):
    model_a, metadata = whisperx.load_align_model(language_code=language, device=None)
    if device is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
    aligned_result = whisperx.align(
        list_of_dict,
        model_a,
        metadata,
        audio.astype(np.float32),
        device,
        return_char_alignments=False,
    )
    return aligned_result


class AudioTranscriber:
    def __init__(
        self,
        language="de",
        device=None,
        sr_rate=16000,
    ):
        self.device = (
            device if device else "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.transcribe_model = whisperx.load_model(
            "i4ds/whisper4sg-srg-v2-full-mc-de-sg-corpus-v2",
            self.device,
        )
        self.language = language
        self.align_model, self.metadata = whisperx.load_align_model(
            device=self.device,
            language_code=self.language,
        )
        self.sr_rate = sr_rate

    def video_to_mp3(self, path):
        # Load the video file
        video = VideoFileClip(path)

        # Extract the audio
        audio = video.audio

        # Mp3 path
        file_path, _ = os.path.splitext(path)
        mp3_path = file_path + ".mp3"

        # Write the audio to an MP3 file
        audio.write_audiofile(mp3_path)

        return mp3_path

    def load_audio_to_numpy(self, audio_path):
        audio_array, sr = torchaudio.load(audio_path)
        if sr != self.sr_rate:
            audio_array = torchaudio.transforms.Resample(sr, self.sr_rate)(audio_array)
        return torch.mean(audio_array, dim=0).numpy()

    def transcribe(self, audio, batch_size=8):
        if isinstance(audio, str):
            if audio.endswith(".mp4"):
                # Video, extract Audio
                audio = self.video_to_mp3(audio)
            audio = self.load_audio_to_numpy(audio_path=audio)

        transcription_result = self.transcribe_model.transcribe(
            audio, batch_size=batch_size, language=self.language
        )

        aligned_result = whisperx.align(
            transcription_result["segments"],
            self.align_model,
            self.metadata,
            audio,
            device=self.device,
            return_char_alignments=False,
        )

        # Create subs
        pred_subs = pysubs2.load_from_whisper(aligned_result)

        return pred_subs
