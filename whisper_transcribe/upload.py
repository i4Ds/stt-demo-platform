import gradio as gr
import os
from utils import handle_upload, UPLOAD_FOLDER

# Configuration
THEME = gr.themes.Soft()

# Ensure the upload and converted folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Create the Gradio interface
with gr.Blocks(theme=THEME) as app:
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
        "The model is currently running on a CPU and thus expect the transcription to take around the same time as the audio length. After selecting your file or drag & drop, click 'Upload' and wait for your transcription to finish."
        "</div>"
    )
    with gr.Row():
        file_input = gr.File(label="Select Audio File")
        upload_button = gr.Button("Upload & Convert")

    output_text = gr.Markdown(label="Upload Status")

    upload_button.click(fn=handle_upload, inputs=[file_input], outputs=[output_text])

# Launch the app
if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7861, root_path="/long_v3")
