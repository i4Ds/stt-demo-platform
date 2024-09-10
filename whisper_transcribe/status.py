import gradio as gr
import os
from utils import UPLOAD_FOLDER
from transcribe import TRANSCRIBED_FOLDER


def check_file_status(uuid: str, request: gr.Request):
    if not uuid:
        return "Error: No file UUID provided. Please enter a UUID."

    # Check in the converted folder
    output_path = os.path.join(UPLOAD_FOLDER, TRANSCRIBED_FOLDER)
    converted_file_path = os.path.join(output_path, f"{uuid}.srt")
    if os.path.exists(converted_file_path):
        return f"File found: {uuid}.srt"

    return f"Error: No file found with UUID {uuid}"


def get_initial_uuid(request: gr.Request):
    return request.query_params.get("uuid", "")


with gr.Blocks() as status_app:
    gr.Markdown("# File Status Checker")

    uuid_input = gr.Textbox(label="File UUID", placeholder="Enter file UUID here")
    check_button = gr.Button("Check Status")
    status_output = gr.Markdown("Status will appear here.")

    check_button.click(fn=check_file_status, inputs=[uuid_input], outputs=status_output)

    # Set initial UUID value from request
    status_app.load(
        fn=get_initial_uuid,
        inputs=None,
        outputs=uuid_input,
    )

if __name__ == "__main__":
    status_app.launch(
        server_name="127.0.0.1", server_port=7862, root_path="/long_v3/status"
    )
