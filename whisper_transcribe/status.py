import gradio as gr
import os
from utils import UPLOAD_FOLDER, convert_srt_to_format
from transcribe import TRANSCRIBED_FOLDER


def check_file_status(request: gr.Request):
    uuid: str = request.query_params.get("uuid", "")
    uuid = uuid.split("/")[-1].replace(".mp3", "")
    if not uuid:
        return (
            "Error: No file UUID provided. Please add a UUID to the URL.\n\n",
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
            gr.update(visible=False),
        )

    output_path = os.path.join(UPLOAD_FOLDER, TRANSCRIBED_FOLDER)
    srt_file_path = os.path.join(output_path, f"{uuid}.srt")

    if os.path.exists(srt_file_path):
        # Read the first 10 lines for preview
        with open(srt_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            preview = "".join(lines[:10])

        # Prepare other format files
        csv_file_path = handle_download(srt_file_path, "csv")
        tsv_file_path = handle_download(srt_file_path, "tsv")
        txt_file_path = handle_download(srt_file_path, "txt")

        return (
            f"**Preview of Transcription:**\n\n{preview}",
            gr.update(visible=True, value=srt_file_path),
            gr.update(visible=True, value=csv_file_path),
            gr.update(visible=True, value=tsv_file_path),
            gr.update(visible=True, value=txt_file_path),
        )
    else:
        return (
            f"Transcription for UUID {uuid} not found. It may still be processing or the UUID is incorrect. This page will auto-refresh every 30 seconds.\n\n",
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
    gr.Markdown(
        """
        # Swiss German Transcription Status Checker

        <div style='font-size: 18px; line-height: 1.5;'>
        <p>Check the status of your Swiss German audio transcription here!</p>
        <p>Your UUID is in the 4th segment of the URL you were redirected to after uploading your file.</p>
        <p>This page will auto-refresh every 30 seconds until your transcription is ready.</p>
        </div>
        """
    )
    preview_output = gr.Markdown("\n\n\n")

    # Initialize DownloadButtons as hidden
    download_srt = gr.DownloadButton("Download SRT", visible=False)
    download_csv = gr.DownloadButton("Download CSV", visible=False)
    download_tsv = gr.DownloadButton("Download TSV", visible=False)
    download_txt = gr.DownloadButton("Download TXT", visible=False)

    status_app.load(
        fn=check_file_status,
        inputs=None,
        outputs=[
            preview_output,
            download_srt,
            download_csv,
            download_tsv,
            download_txt,
        ],
        show_api=False,
        js="""
        async () => {
            let counter = 0;
            const refreshInterval = setInterval(async () => {
                counter++;
                document.getElementById('refresh_counter').textContent = counter;
                
                // Check if any download button is visible
                const downloadButtons = document.querySelectorAll('button[id^="component-"][id$="-download-srt"], button[id^="component-"][id$="-download-csv"], button[id^="component-"][id$="-download-tsv"], button[id^="component-"][id$="-download-txt"]');
                const isAnyButtonVisible = Array.from(downloadButtons).some(button => !button.hidden);
                
                if (isAnyButtonVisible || counter >= 60) {  // Stop after 30 minutes (60 * 30 seconds)
                    clearInterval(refreshInterval);
                    console.log('Auto-refresh stopped');
                } else {
                    await document.getElementsByTagName('gradio-app')[0].querySelector('div[id^="component-"]').props.load();
                }
            }, 30000);  // Refresh every 30 seconds
        }
        """,
    )

if __name__ == "__main__":
    print("Launching Swiss German Transcription Status Checker...")
    print(
        "Access the app by navigating to http://127.0.0.1:7862/long_v3/status?uuid=YOUR_UUID_HERE"
    )
    status_app.launch(
        server_name="127.0.0.1", server_port=7862, root_path="/long_v3/status"
    )
