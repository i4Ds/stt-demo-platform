import gradio as gr
import os
from utils import UPLOAD_FOLDER
from transcribe import TRANSCRIBED_FOLDER


def check_file_status(uuid: str):
    if not uuid:
        return "Error: No file UUID provided. Please add a UUID to the URL.", gr.File(
            visible=False
        )

    output_path = os.path.join(UPLOAD_FOLDER, TRANSCRIBED_FOLDER)
    converted_file_path = os.path.join(output_path, f"{uuid}.srt")
    if os.path.exists(converted_file_path):
        return f"File is ready: {uuid}.srt", gr.File(
            value=converted_file_path, visible=True
        )

    return (
        f"Processing file with UUID {uuid}. This page will automatically update every 15 seconds.",
        gr.File(visible=False),
    )


def get_initial_uuid(request: gr.Request):
    return request.query_params.get("uuid", "")


with gr.Blocks() as status_app:
    gr.Markdown("# File Status Checker")

    uuid_display = gr.Markdown("Checking status...")
    status_output = gr.Markdown("Status will appear here.")
    download_link = gr.File(label="Download File", visible=False)

    def update_status(uuid):
        status, download = check_file_status(uuid)
        return uuid, status, download

    status_app.load(
        fn=get_initial_uuid,
        inputs=None,
        outputs=uuid_display,
    ).then(
        fn=update_status,
        inputs=[uuid_display],
        outputs=[uuid_display, status_output, download_link],
        every=15,  # Auto-update every 15 seconds
    )

if __name__ == "__main__":
    status_app.launch(
        server_name="127.0.0.1", server_port=7862, root_path="/long_v3/status"
    )
