import gradio as gr
import os
import time

UPLOAD_FOLDER = "uploads"
THEME = gr.themes.Soft()
CHECK_INTERVAL = 15  # seconds


def check_status(uuid):
    if not uuid:
        return "Invalid UUID. Please check the URL and try again."

    mp3_file = f"{uuid}.mp3"
    mp3_path = os.path.join(UPLOAD_FOLDER, "converted", mp3_file)

    if not os.path.exists(mp3_path):
        return "File not found. Please check your UUID."

    srt_file = f"{uuid}.srt"
    srt_path = os.path.join(UPLOAD_FOLDER, srt_file)

    while True:
        if os.path.exists(srt_path):
            with open(srt_path, "r") as file:
                transcription = file.read()
            return f"Transcription complete:\n\n{transcription}"
        else:
            yield "Transcription in progress. Please wait..."
            time.sleep(CHECK_INTERVAL)


with gr.Blocks(theme=THEME) as app:
    gr.Markdown("# Transcription Status")
    uuid_input = gr.Textbox(label="Enter UUID")
    check_button = gr.Button("Check Status")
    status_output = gr.Markdown(label="Status")

    check_button.click(fn=check_status, inputs=[uuid_input], outputs=[status_output])

if __name__ == "__main__":
    app.launch(server_name="127.0.0.1", server_port=7861)
