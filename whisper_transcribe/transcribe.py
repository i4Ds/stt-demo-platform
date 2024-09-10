import pysubs2
import torch
import whisperx
import torchaudio
from whisperx.alignment import DEFAULT_ALIGN_MODELS_HF
from utils import convert_to_mp3_16khz, UPLOAD_FOLDER, CONVERTED_FOLDER
import os
import shutil
import time

DEFAULT_ALIGN_MODELS_HF["de"] = "scasutt/wav2vec2-large-xlsr-52_Swiss_German"
PROCESSED_FOLDER = "processed"
TRANSCRIPED_FOLDER = "transcribed"


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
            compute_type="float16" if torch.cuda.is_available() else "float32",
        )
        self.language = language
        self.align_model, self.metadata = whisperx.load_align_model(
            device=self.device,
            language_code=self.language,
        )
        self.sr_rate = sr_rate

    def load_audio_to_numpy(self, audio_path):
        audio_array, sr = torchaudio.load(audio_path)
        if sr != self.sr_rate:
            audio_array = torchaudio.transforms.Resample(sr, self.sr_rate)(audio_array)
        return torch.mean(audio_array, dim=0).numpy()

    def transcribe(self, audio, batch_size=16):
        if isinstance(audio, str):
            if not audio.endswith(".mp3"):
                # Video, extract Audio
                audio = convert_to_mp3_16khz(audio)
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


if __name__ == "__main__":
    audio_transcriber = AudioTranscriber()
    input_mp3s = os.path.join(UPLOAD_FOLDER, CONVERTED_FOLDER)
    output_mp3s = os.path.join(UPLOAD_FOLDER, PROCESSED_FOLDER)

    while True:
        audio_files = [f for f in os.listdir(input_mp3s) if f.endswith(".mp3")]

        if audio_files:
            print(f"Found {len(audio_files)} new files to process.")
            for audio_file in audio_files:
                print(f"Processing {audio_file}")
                # Make paths
                input_path = os.path.join(input_mp3s, audio_file)
                output_path = os.path.join(output_mp3s, audio_file)
                transcription_path = os.path.join(
                    TRANSCRIPED_FOLDER, f"{os.path.splitext(audio_file)[0]}.srt"
                )

                # Transcribe the audio file
                transcription: pysubs2.SSAFile = audio_transcriber.transcribe(
                    input_path
                )

                transcription.save(transcription_path)

                # Move the processed audio file
                shutil.move(input_path, output_path)

                print(f"Processed and moved: {audio_file}")
        else:
            print("No new files to process. Sleeping for 1 second...")
            time.sleep(1)
