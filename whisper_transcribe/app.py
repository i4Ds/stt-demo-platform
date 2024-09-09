import torch
import gradio as gr
from transcribe import AudioTranscriber
import time
import tempfile
from pysubs2 import SSAFile
import csv
import io

audio_transcriber = AudioTranscriber()

device = 0 if torch.cuda.is_available() else "cpu"
THEME = gr.themes.Soft()


def transcribe(inputs):
    if inputs is None:
        raise gr.Error(
            "No audio file submitted! Please upload or record an audio file before submitting your request."
        )

    start_time = time.time()
    pred_sub = audio_transcriber.transcribe(inputs)
    end_time = time.time()

    transcription_time = (end_time - start_time) / 60  # Convert to minutes

    # Add metadata to the subtitle file
    pred_sub.info["Transcribed by"] = "i4ds"
    pred_sub.info["URL"] = "https://stt4sg.fhnw.ch/long_v2"
    pred_sub.info["Transcription Time"] = f"{transcription_time:.2f} minutes"

    return pred_sub, pred_sub.to_string(format_="srt")


def update_text(subs, include_timestamps):
    return sub_to_text(subs, include_timestamps)


def sub_to_text(subs: SSAFile, include_timestamps: bool):
    sub_text = subs.to_string(format_="srt")

    if not include_timestamps:
        # Remove timestamp information
        lines = sub_text.split("\n")
        sub = "\n".join(
            [
                line
                for line in lines
                if not line.strip().isdigit() and not " --> " in line
            ]
        )
        return sub
    else:
        return sub_text


def subs_to_Xsv(subs: SSAFile, include_timestamps: bool, sep: str = ","):
    output = io.StringIO()
    writer = csv.writer(output)

    if include_timestamps:
        writer.writerow(["Start", "End", "Text"])
        for sub in subs:
            writer.writerow([sub.start, sub.end, sub.text])
    else:
        writer.writerow(["Text"])
        for sub in subs:
            writer.writerow([sub.text])

    return output.getvalue()


def prepare_download(subs, file_format, include_timestamps):
    if subs is None:
        raise gr.Error(
            "No subtitles available for download. Please transcribe an audio file first."
        )
    if file_format == "srt":
        sub_text = sub_to_text(subs, include_timestamps)
    elif file_format == "txt":
        sub_text = sub_to_text(subs, include_timestamps)
    elif file_format == "csv":
        sub_text = subs_to_Xsv(subs, include_timestamps)
    elif file_format == "tsv":
        sub_text = subs_to_Xsv(subs, include_timestamps, sep="\t")
    else:
        raise ValueError(f"Unsupported file format: {file_format}")

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=f".{file_format}"
    ) as temp_file:
        temp_file.write(sub_text)
        temp_file_path = temp_file.name

    return temp_file_path


demo = gr.Blocks(theme=THEME)

with demo:
    gr.Markdown("# Swiss German Whisper")
    gr.Markdown(
        "<div style='font-size: 18px; line-height: 1.5;'>"
        "<p>Transcribe Swiss German audio of up to 15 minutes with a click!</p>"
        "<p>This demo uses a model trained on Swiss German Data by the "
        "<a href='https://stt4sg.fhnw.ch/' style='color: #007bff; text-decoration: none;'>NLP Team at i4ds</a>, "
        "supervised by Prof. Dr. Manfred Vogel.</p>"
        "<p>It combines:"
        "<ul>"
        "<li><a href='https://github.com/guillaumekln/faster-whisper' style='color: #007bff; text-decoration: none;'>SYSTRAN/faster-whisper</a> for fast transcription</li>"
        "<li><a href='https://github.com/m-bain/whisperX' style='color: #007bff; text-decoration: none;'>m-bain/whisperX</a> for precise word-level timestamps</li>"
        "</ul>"
        "</p>"
        "The model is currently running on a CPU and thus expect the transcription to take around the same time as the audio length (keep the window open!)."
        "</div>"
    )

    with gr.Tabs():
        with gr.TabItem("Audio File"):
            audio_file = gr.Audio(sources="upload", type="filepath", label="Audio file")
            transcribe_button = gr.Button("Transcribe")

        with gr.TabItem("Microphone"):
            audio_mic = gr.Audio(sources="microphone", type="filepath")
            transcribe_mic_button = gr.Button("Transcribe")

    output_text = gr.Textbox(label="Transcription")

    with gr.Row():
        file_format = gr.Dropdown(
            choices=["txt", "srt", "csv", "tsv"], label="File Format", value="txt"
        )
        include_timestamps = gr.Checkbox(label="Include timestamps", value=True)

    download_button = gr.Button("Process transcription")

    file_output = gr.File(label="Downloads")

    subs = gr.State()

    transcribe_button.click(
        transcribe, inputs=[audio_file], outputs=[subs, output_text]
    )

    transcribe_mic_button.click(
        transcribe, inputs=[audio_mic], outputs=[subs, output_text]
    )

    download_button.click(
        prepare_download,
        inputs=[subs, file_format, include_timestamps],
        outputs=[file_output],
    )

demo.launch(server_name="127.0.0.1", server_port=7860, root_path="/long_v2")
