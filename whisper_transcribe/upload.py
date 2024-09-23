import gradio as gr
import os
from utils import handle_upload, UPLOAD_FOLDER

# Configuration
THEME = gr.themes.Soft()

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Create the Gradio interface
with gr.Blocks(theme=THEME) as app:
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
        <p><strong>Transcribe Swiss German audio files of up to 500MB!</strong></p>
        <p>This demo uses a model trained on Swiss German data by the 
        <a href="https://stt4sg.fhnw.ch/" target="_blank">NLP Team at i4ds</a>, supervised by Prof. Dr. Manfred Vogel.</p>
        <p>It combines:</p>
        <ul>
            <li><a href="https://github.com/guillaumekln/faster-whisper" target="_blank">SYSTRAN/faster-whisper</a> for fast transcription</li>
            <li><a href="https://github.com/m-bain/whisperX" target="_blank">m-bain/whisperX</a> for precise word-level timestamps</li>
        </ul>
        <p><strong>Note:</strong> The model is currently running on a CPU, so expect the transcription to take around the same time as the audio length.</p>
    </div>
    """
    )

    # Instructions Box
    gr.HTML(
        """
    <div class="instructions-box">
        <p><strong>Instructions:</strong></p>
        <ol>
            <li>Select or drag & drop your audio file (up to 500MB).</li>
            <li>Wait for the file to upload completely.</li>
            <li>Click on <em>'Convert & Transcribe'</em>.</li>
            <li>Go to the status page (which appears after clicking <em>'Convert & Transcribe'</em>) to monitor the transcription progress and download the transcription file once it's ready.</li>
        </ol>
    </div>
    """
    )

    # File Input and Button
    with gr.Row():
        file_input = gr.File(label="Select & Upload Audio File")
        upload_button = gr.Button("Convert & Transcribe")

    # Output Text
    output_text = gr.Markdown(label="Upload Status")

    # Define the button click action
    upload_button.click(fn=handle_upload, inputs=[file_input], outputs=[output_text])

# Launch the app
if __name__ == "__main__":
    print("Launching Swiss German Whisper App...")
    print(
        "Access the app by navigating to http://127.0.0.1:7861/long_v3 in your web browser."
    )
    app.launch(server_name="127.0.0.1", server_port=7861, root_path="/long_v3")
