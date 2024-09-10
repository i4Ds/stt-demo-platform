import gradio as gr
import uuid
import os
import shutil
from utils import convert_to_mp3_16khz

# Configuration
UPLOAD_FOLDER = "uploads"
THEME = gr.themes.Soft()
BASE_URL = "https://stt4sg.fhnw.ch"  # Replace with your actual base URL

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def save_uploaded_file(file):
    if file is None:
        return None

    # Generate a UUID for the file
    file_uuid = str(uuid.uuid4())

    # Get the file extension
    _, file_extension = os.path.splitext(file.name)

    # Create the new filename with UUID
    new_filename = f"{file_uuid}{file_extension}"

    # Save the file
    original_path = os.path.join(UPLOAD_FOLDER, new_filename)
    shutil.copy(file.name, original_path)

    conversion_result = convert_to_mp3_16khz(original_path)

    if conversion_result:
        # Optionally, remove the original file to save space
        os.remove(original_path)
        print(f"Converted and saved as MP3: {conversion_result}")
    else:
        print(f"Conversion failed. Original file retained: {original_path}")

    return file_uuid


def handle_upload(file):
    if file is None:
        raise gr.Error("No file uploaded. Please upload an audio file.")

    file_uuid = save_uploaded_file(file)
    if file_uuid:
        status_url = f"{BASE_URL}/status/{file_uuid}"
        return f"File uploaded & converted successfully. Check the status here: [Transcription Status]({status_url})"
    else:
        raise gr.Error("Failed to upload file. Please try again.")


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
        "The model is currently running on a CPU and thus expect the transcription to take around the same time as the audio length. After selecting your file or drag & drop, click 'Upload' and then follow the link to check the status of your transcription."
        "</div>"
    )
    with gr.Row():
        file_input = gr.File(label="Upload Audio File")
        upload_button = gr.Button("Upload")

    output_text = gr.Markdown(label="Upload Status")

    upload_button.click(fn=handle_upload, inputs=[file_input], outputs=[output_text])

# Launch the app
if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7861, root_path="/long_v3")
