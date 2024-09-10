import gradio as gr
import os
from utils import UPLOAD_FOLDER, convert_srt_to_format
from transcribe import TRANSCRIBED_FOLDER
import tempfile


def check_file_status(uuid: str):
    if not uuid:
        return "Error: No file UUID provided. Please add a UUID to the URL.", None

    output_path = os.path.join(UPLOAD_FOLDER, TRANSCRIBED_FOLDER)
    srt_file_path = os.path.join(output_path, f"{uuid}.srt")

    if os.path.exists(srt_file_path):
        return f"File is ready: {uuid}.srt", srt_file_path

    return (
        f"File with UUID {uuid} not found. It may still be processing or the UUID is incorrect. Please refresh the page to check again.",
        None,
    )


def get_initial_uuid(request: gr.Request):
    return request.query_params.get("uuid", "")


def handle_download(file_path, format):
    if not file_path or not format:
        return None
    content = convert_srt_to_format(file_path, format)
    if content.startswith("Error"):
        return content

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=f".{format}"
    ) as temp_file:
        temp_file.write(content)
        temp_file_path = temp_file.name

    return temp_file_path


with gr.Blocks() as status_app:
    gr.Markdown(
        """
        # Swiss German Transcription Status Checker

        <div style='font-size: 18px; line-height: 1.5;'>
        <p>Check the status of your Swiss German audio transcription here!</p>
        <p>The UUID from your file upload should be in the URL. If your file isn't ready yet, simply refresh the page to check again.</p>
        </div>
        """
    )

    uuid_display = gr.Markdown("Checking status...")
    status_output = gr.Markdown("Status will appear here.")
    format_dropdown = gr.Dropdown(
        choices=["srt", "csv", "tsv", "txt"],
        label="Select download format",
        value="srt",
        visible=False,
    )
    download_button = gr.Button("Generate", visible=False)
    file_path_state = gr.State(None)
    download_file = gr.File(label="Available Files", visible=True)

    def update_status(uuid):
        status, file_path = check_file_status(uuid)
        downloads_visible = file_path is not None
        return (
            uuid,
            status,
            gr.update(visible=downloads_visible),
            gr.update(visible=downloads_visible),
            file_path,
        )

    status_app.load(
        fn=get_initial_uuid,
        inputs=None,
        outputs=uuid_display,
    ).then(
        fn=update_status,
        inputs=[uuid_display],
        outputs=[
            uuid_display,
            status_output,
            format_dropdown,
            download_button,
            file_path_state,
        ],
    )

    download_button.click(
        fn=handle_download,
        inputs=[file_path_state, format_dropdown],
        outputs=download_file,
    )

if __name__ == "__main__":
    status_app.launch(
        server_name="127.0.0.1", server_port=7862, root_path="/long_v3/status"
    )
