import torch
import gradio as gr
from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment
from pydub import AudioSegment, effects
import os
from datetime import datetime
import csv


THEME = gr.themes.Soft()
MODEL = "i4ds/whisper4sg-srg-v2-full-mc-de-sg-corpus-v2"
FOLDER = "data"
CSV_PATH = FOLDER + "/data.csv"

device = "cuda" if torch.cuda.is_available() else "cpu"
model = WhisperModel(MODEL, device=device, compute_type="int8")


def transcribe(path: str, csv_path: str = CSV_PATH) -> tuple[str, list]:
    if path is None or os.stat(path).st_size < 1024 * 10:  # 5 KB
        return ""

    # Normalize audio
    audio = AudioSegment.from_file(path)
    normalized_audio = effects.normalize(audio)

    # Create a timestamp for the audio name
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    audio_filename = f"{timestamp}_normalized.mp3"
    normalized_audio_path = os.path.join(FOLDER, audio_filename)

    # Export the normalized audio
    normalized_audio.export(normalized_audio_path, format="mp3")

    with torch.inference_mode():
        segments, _ = model.transcribe(
            normalized_audio_path,
            language="de",
            without_timestamps=True,
            vad_filter=False,
        )

        # Convert segments to text
        text = fw_segments_to_text(segments)

        # Append the result to a CSV file
        with open(csv_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([audio_filename, text])

        # Return the transcribed text
        return text


def fw_segments_to_text(segments: list[Segment]) -> str:
    return " ".join(segment.text for segment in segments).strip()


app = gr.Blocks(theme=THEME)

with app:
    # Include custom CSS for styling
    gr.HTML(
        """
    <style>
    .info-box {
        border: 1px solid #ccc;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
    }
    .instructions-box {
        border: 1px solid #007bff;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
    }
    </style>
    """
    )

    # Title
    gr.Markdown("# Swiss German Whisper")

    # Information Box
    gr.HTML(
        """
    <div class="info-box">
        <p><strong>Transcribe Swiss German audio live in your Browser!</strong></p>
        <p>This demo uses a model trained on Swiss German data by the 
        <a href="https://stt4sg.fhnw.ch/" target="_blank">NLP Team at i4ds</a>, supervised by Prof. Dr. Manfred Vogel.</p>
        <p>It combines:</p>
        <ul>
            <li><a href="https://github.com/guillaumekln/faster-whisper" target="_blank">SYSTRAN/faster-whisper</a> for fast transcription</li>
        </ul>
        <p><strong>Note:</strong> The int8-quantized model is currently running on a CPU, so expect more latency and maybe a lower quality.<p>
    </div>
    """
    )

    # Instructions Box
    gr.HTML(
        """
    <div class="instructions-box">
        <p><strong>Instructions:</strong></p>
        <ol>
            <li>Click on <em>Record from microphone</em> to start recording.</li>
            <li>Stop recording by clicking on <em>Stop</em>.</li>
            <li>Click on <em>Submit</em>.</li>
            <li>Wait for the transcription to complete.</li>
        </ol>
    </div>
    """
    )
    gr.Interface(
        fn=transcribe,
        inputs=[
            gr.Audio(sources="microphone", type="filepath"),
        ],
        outputs="text",
        theme=THEME,
        allow_flagging="never",
    )

app.launch(server_name="127.0.0.1", server_port=7863, root_path="/stt")
