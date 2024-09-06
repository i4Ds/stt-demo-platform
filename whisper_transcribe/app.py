import torch

import gradio as gr
from transcribe import AudioTranscriber


audio_transcriber = AudioTranscriber()

device = 0 if torch.cuda.is_available() else "cpu"


def transcribe(inputs, task):
    if inputs is None:
        raise gr.Error(
            "No audio file submitted! Please upload or record an audio file before submitting your request."
        )
    pred_sub = audio_transcriber.transcribe(inputs)
    # Extract the transcription from the output
    return pred_sub.to_string(format_="srt")


demo = gr.Blocks()

mf_transcribe = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(sources="microphone", type="filepath"),
        gr.Radio(["transcribe"], label="Task", value="transcribe"),
    ],
    outputs="text",
    theme="huggingface",
    title="Swiss German Whisper",
    description=(
        "Transcribe Swiss German audio from your microphone! This demo uses a model trained on Swiss German Data "
        "by the NLP Team at i4ds, supervised by Prof. Dr. Manfred Vogel. It combines SYSTRAN/faster-whisper for "
        "efficient transcription and m-bain/whisperX for precise word-level timestamps, delivering accurate Swiss "
        "German transcriptions with enhanced timing features."
    ),
    allow_flagging="never",
)

file_transcribe = gr.Interface(
    fn=transcribe,
    inputs=[
        gr.Audio(sources="upload", type="filepath", label="Audio file"),
        gr.Radio(["transcribe"], label="Task", value="transcribe"),
    ],
    outputs="text",
    theme="huggingface",
    title="Swiss German Whisper",
    description=(
        "Transcribe Swiss German audio of any length with a click! This demo uses a model trained on Swiss German Data "
        "by the NLP Team at i4ds, supervised by Prof. Dr. Manfred Vogel. It combines SYSTRAN/faster-whisper for "
        "efficient transcription and m-bain/whisperX for precise word-level timestamps, delivering accurate Swiss "
        "German transcriptions with enhanced timing features."
    ),
    allow_flagging="never",
)

with demo:
    gr.TabbedInterface(
        [mf_transcribe, file_transcribe],
        ["Microphone", "Audio file", "YouTube"],
    )

demo.launch(server_name="127.0.0.1", server_port=7860, share=True)
