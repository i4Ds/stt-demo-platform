import torch

import gradio as gr
from transcribe import AudioTranscriber
import time

audio_transcriber = AudioTranscriber()

device = 0 if torch.cuda.is_available() else "cpu"


def transcribe(inputs):
    if inputs is None:
        raise gr.Error(
            "No audio file submitted! Please upload or record an audio file before submitting your request."
        )

    start_time = time.time()
    pred_sub = audio_transcriber.transcribe(inputs)
    end_time = time.time()

    transcription_time = (end_time - start_time) / 60  # Convert to minutes

    # Extract the transcription from the output
    transcription = pred_sub.to_string(format_="srt")

    # Add the requested information
    footer = f"\n\nTranscribed by i4ds\nURL: https://stt4sg.fhnw.ch/long_v2\nTranscription took {transcription_time:.2f} minutes"

    return transcription + footer


demo = gr.Blocks()

file_transcribe = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(sources="upload", type="filepath", label="Audio file"),
    ],
    outputs="text",
    theme="huggingface",
    title="Swiss German Whisper",
    description=(
        "<div style='font-size: 18px; line-height: 1.5;'>"
        "<p>Transcribe Swiss German audio of up to 15 minutes with a click!</p>"
        "<p>This demo uses a model trained on Swiss German Data by the "
        "<a href='https://stt4sg.fhnw.ch/home' style='color: #007bff; text-decoration: none;'>NLP Team at i4ds</a>, "
        "supervised by Prof. Dr. Manfred Vogel.</p>"
        "<p>It combines:"
        "<ul>"
        "<li><a href='https://github.com/guillaumekln/faster-whisper' style='color: #007bff; text-decoration: none;'>SYSTRAN/faster-whisper</a> for fast transcription</li>"
        "<li><a href='https://github.com/m-bain/whisperX' style='color: #007bff; text-decoration: none;'>m-bain/whisperX</a> for precise word-level timestamps</li>"
        "</ul>"
        "</p>"
        "The model is currently running on a CPU and thus expect the transcription to take around the same time as the audio length (keep the window open!)."
        "</div>"
    ),
    allow_flagging="never",
)


mf_transcribe = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(sources="microphone", type="filepath"),
    ],
    outputs="text",
    theme="huggingface",
    title="Swiss German Whisper",
    description=(
        "<div style='font-size: 18px; line-height: 1.5;'>"
        "<p>Transcribe Swiss German audio from your microphone!</p>"
        "<p>This demo uses a model trained on Swiss German Data by the "
        "<a href='https://stt4sg.fhnw.ch/home' style='color: #007bff; text-decoration: none;'>NLP Team at i4ds</a>, "
        "supervised by Prof. Dr. Manfred Vogel.</p>"
        "<p>It combines:"
        "<ul>"
        "<li><a href='https://github.com/guillaumekln/faster-whisper' style='color: #007bff; text-decoration: none;'>SYSTRAN/faster-whisper</a> for fast transcription</li>"
        "<li><a href='https://github.com/m-bain/whisperX' style='color: #007bff; text-decoration: none;'>m-bain/whisperX</a> for precise word-level timestamps</li>"
        "</ul>"
        "</p>"
        "</div>"
    ),
    allow_flagging="never",
)


with demo:
    gr.TabbedInterface(
        [file_transcribe, mf_transcribe],
        ["Audio file", "Microphone"],
    )

demo.launch(server_name="127.0.0.1", server_port=7860)
