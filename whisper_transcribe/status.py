import gradio as gr
import os
from utils import UPLOAD_BASE_FOLDER, convert_srt_to_format
from transcribe import TRANSCRIBED_FOLDER


def check_file_status(request: gr.Request):
    uuid: str = request.query_params.get("uuid", "")
    uuid = uuid.split("/")[-1].replace(".mp3", "")
    if not uuid:
        error_message = (
            "<div class='error-box'>"
            "<strong>Error:</strong> No file UUID provided. Please add a UUID to the URL."
            "</div>"
        )
        return (
            error_message,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
        )

    output_path = os.path.join(UPLOAD_BASE_FOLDER, TRANSCRIBED_FOLDER)
    srt_file_path = os.path.join(output_path, f"{uuid}.srt")

    if os.path.exists(srt_file_path):
        # Prepare other format files
        csv_file_path = handle_download(srt_file_path, "csv")
        tsv_file_path = handle_download(srt_file_path, "tsv")
        txt_file_path = handle_download(srt_file_path, "txt")

        # Read the first 20 lines for preview
        with open(txt_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            preview = "".join(lines[:20])
            formatted_preview = (
                f"<div class='preview-box'>"
                f"<h2>Preview of your Transcription:</h2>"
                f"<pre>{preview}</pre>"
                f"</div>"
            )

        return (
            formatted_preview,
            gr.update(visible=True),
            gr.update(visible=True, value=srt_file_path),
            gr.update(visible=True, value=csv_file_path),
            gr.update(visible=True, value=tsv_file_path),
            gr.update(visible=True, value=txt_file_path),
        )
    else:
        error_message = (
            f"<div class='error-box'>"
            f"<strong>Transcription not found:</strong> UUID {uuid} not found. Please refresh the page to check again."
            f"</div>"
        )
        return (
            error_message,
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
        )


def handle_download(file_path, format):
    if not file_path or not format:
        return None

    content = convert_srt_to_format(file_path, format)
    if content.startswith("Error"):
        return None

    new_file_path = file_path.replace(".srt", f".{format}")

    # Write the content to the new file
    with open(new_file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return new_file_path


with gr.Blocks() as status_app:
    # Include custom CSS for styling
    gr.HTML(
        """
    <style>
    .info-box {
        border: 1px solid #ccc;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .error-box {
        border: 1px solid #ff4d4d;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
        margin-bottom: 20px;
    }
    .preview-box {
        border: 1px solid #007bff;
        padding: 15px;
        border-radius: 5px;
        font-size: 16px;
        margin-bottom: 20px;
        overflow: auto;
        max-height: 300px;
    }
    pre {
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 0;
    }
    </style>
    """
    )

    # Title
    gr.Markdown("# Swiss German Transcription Status Checker")

    # Information Box
    gr.HTML(
        """
    <div class="info-box">
        <p><strong>Check the status of your Swiss German audio transcription here!</strong></p>
        <p>If not availabe, please refresh the page to check again.</p>
    </div>
    """
    )

    # Preview Output
    preview_output = gr.HTML()

    # Download Buttons (initially hidden)
    with gr.Row(visible=False) as download_row:
        download_srt = gr.DownloadButton("Download SRT")
        download_csv = gr.DownloadButton("Download CSV")
        download_tsv = gr.DownloadButton("Download TSV")
        download_txt = gr.DownloadButton("Download TXT")

    # Define the function to update visibility based on outputs
    def update_visibility(preview_html, srt_path, csv_path, tsv_path, txt_path):
        if "error-box" in preview_html:
            return {
                preview_output: gr.update(value=preview_html),
                download_row: gr.update(visible=False),
            }
        else:
            return {
                preview_output: gr.update(value=preview_html),
                download_row: gr.update(visible=True),
                download_srt: gr.update(value=srt_path, visible=True),
                download_csv: gr.update(value=csv_path, visible=True),
                download_tsv: gr.update(value=tsv_path, visible=True),
                download_txt: gr.update(value=txt_path, visible=True),
            }

    # Set up the app to load the status on page load
    status_app.load(
        fn=check_file_status,
        inputs=None,
        outputs=[
            preview_output,
            download_row,
            download_srt,
            download_csv,
            download_tsv,
            download_txt,
        ],
        show_api=False,
        postprocess=update_visibility,
    )

if __name__ == "__main__":
    print("Launching Swiss German Transcription Status Checker...")
    print(
        "Access the app by navigating to http://127.0.0.1:7862/long_v3/status?uuid=YOUR_UUID_HERE"
    )
    status_app.launch(
        server_name="127.0.0.1", server_port=7862, root_path="/long_v3/status"
    )
