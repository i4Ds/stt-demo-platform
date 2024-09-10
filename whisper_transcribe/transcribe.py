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
TRANSCRIBED_FOLDER = "transcribed"


def is_file_locked(file_path):
    lock_path = file_path + ".lock"
    if os.path.exists(lock_path):
        return True
    else:
        return False


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

    def transcribe(self, audio, batch_size=8):
        if isinstance(audio, str):
            if not audio.endswith(".mp3"):
                # Video, extract Audio
                audio = convert_to_mp3_16khz(audio)
            audio = self.load_audio_to_numpy(audio_path=audio)

        transcription_result = self.transcribe_model.transcribe(
            audio,
            batch_size=batch_size,
            language=self.language,
            print_progress=True,
            combined_progress=True,
        )

        aligned_result = whisperx.align(
            transcription_result["segments"],
            self.align_model,
            self.metadata,
            audio,
            device=self.device,
            return_char_alignments=False,
            print_progress=True,
            combined_progress=True,
        )

        # Create subs
        pred_subs = pysubs2.load_from_whisper(aligned_result)

        return pred_subs


if __name__ == "__main__":
    audio_transcriber = AudioTranscriber()
    # Create path and folders
    input_mp3s = os.path.join(UPLOAD_FOLDER, CONVERTED_FOLDER)
    output_mp3s = os.path.join(UPLOAD_FOLDER, PROCESSED_FOLDER)
    output_srts = os.path.join(UPLOAD_FOLDER, TRANSCRIBED_FOLDER)
    error_folder = os.path.join(UPLOAD_FOLDER, "trans_error")
    os.makedirs(output_mp3s, exist_ok=True)
    os.makedirs(output_srts, exist_ok=True)
    os.makedirs(error_folder, exist_ok=True)

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
                    output_srts, f"{os.path.splitext(audio_file)[0]}.srt"
                )
                if is_file_locked(os.path.join(input_mp3s, audio_file)):
                    print(f"File {audio_file} is locked. Skipping for now.")
                    continue
                else:
                    try:
                        # Transcribe the audio file
                        transcription: pysubs2.SSAFile = audio_transcriber.transcribe(
                            input_path
                        )

                        transcription.save(transcription_path)

                        # Move the processed audio file
                        shutil.move(input_path, output_path)

                        print(f"Processed and moved: {audio_file}")
                    except Exception as e:
                        print(f"Error processing {audio_file}: {e}")
                        # Move the file to error folder
                        shutil.move(input_path, os.path.join(error_folder, audio_file))
        else:
            time.sleep(5)
