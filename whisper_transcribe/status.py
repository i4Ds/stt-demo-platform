import gradio as gr
import os
from utils import UPLOAD_FOLDER, convert_srt_to_format
from transcribe import TRANSCRIBED_FOLDER
import tempfile


def check_file_status(request: gr.Request):
    uuid = request.query_params.get("uuid", "")
    if not uuid:
        return (
            "Error: No file UUID provided. Please add a UUID to the URL.",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            None,
        )

    output_path = os.path.join(UPLOAD_FOLDER, TRANSCRIBED_FOLDER)
    srt_file_path = os.path.join(output_path, f"{uuid}.srt")

    if os.path.exists(srt_file_path):
        return (
            f"File is ready: {uuid}.srt",
            gr.update(visible=True),
            gr.update(visible=True),
            gr.update(visible=True),
            srt_file_path,
        )
    else:
        return (
            f"File with UUID {uuid} not found. It may still be processing or the UUID is incorrect. Please refresh the page to check the status again.",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            None,
        )


def handle_download(file_path, format):
    if not file_path or not format:
        return None

    content = convert_srt_to_format(file_path, format)
    if content.startswith("Error"):
        return content

    new_file_path = file_path.replace(".srt", f".{format}")

    # Write the content to the new file
    with open(new_file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return new_file_path


with gr.Blocks() as status_app:
    gr.Markdown(
        """
        # Swiss German Transcription Status Checker

        <div style='font-size: 18px; line-height: 1.5;'>
        <p>Check the status of your Swiss German audio transcription here!</p>
        <p>If your file is available, select your preferred format and click "Generate".</p>
        </div>
        """
    )

    status_output = gr.Markdown("Checking status...")
    format_dropdown = gr.Dropdown(
        choices=["srt", "csv", "tsv", "txt"],
        label="Select download format",
        value="srt",
        visible=False,
    )
    download_button = gr.Button("Generate", visible=False)
    file_path_state = gr.State(None)
    download_file = gr.File(label="Available Files", visible=False)

    status_app.load(
        fn=check_file_status,
        inputs=None,
        outputs=[
            status_output,
            format_dropdown,
            download_button,
            download_file,
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
