import gradio as gr
import os
import tempfile
from utils import UPLOAD_FOLDER, convert_srt_to_format
from transcribe import TRANSCRIBED_FOLDER


def check_file_status(uuid: str):
    if not uuid:
        return "Error: No file UUID provided. Please add a UUID to the URL.", None

    output_path = os.path.join(UPLOAD_FOLDER, TRANSCRIBED_FOLDER)
    srt_file_path = os.path.join(output_path, f"{uuid}.srt")

    if os.path.exists(srt_file_path):
        return f"File is ready: {uuid}.srt", srt_file_path

    return (
        f"Processing file with UUID {uuid}. Please refresh the page to check again.",
        None,
    )


def get_initial_uuid(request: gr.Request):
    return request.query_params.get("uuid", "")


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


def handle_download(file_path, format):
    if not file_path or not format:
        return None, "No file available for download."
    content = convert_srt_to_format(file_path, format)
    if content.startswith("Error"):
        return None, content

    with tempfile.NamedTemporaryFile(
        mode="w", delete=False, suffix=f".{format}"
    ) as temp_file:
        temp_file.write(content)
        return temp_file.name, f"File converted to {format}. Click to download."


with gr.Blocks() as status_app:
    gr.Markdown("# Transcription Status")

    uuid_display = gr.Markdown("Checking status...")
    status_output = gr.Markdown("Status will appear here.")
    format_dropdown = gr.Dropdown(
        choices=["srt", "csv", "tsv", "txt"],
        label="Select download format",
        value="srt",
        visible=False,
    )
    download_button = gr.Button("Convert and Download", visible=False)
    file_path_state = gr.State(None)
    download_file = gr.File(label="Download File", visible=False)
    download_status = gr.Markdown(visible=False)

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
        outputs=[download_file, download_status],
    ).then(
        lambda: (gr.update(visible=True), gr.update(visible=True)),
        None,
        [download_file, download_status],
    )

if __name__ == "__main__":
    status_app.launch(
        server_name="127.0.0.1", server_port=7862, root_path="/long_v3/status"
    )
