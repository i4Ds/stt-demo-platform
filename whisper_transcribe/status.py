import gradio as gr
import os

# Assuming these folders are defined and exist
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = os.path.join(UPLOAD_FOLDER, "converted")


def check_file_status(request: gr.Request):
    params = request.query_params
    file_uuid = params.get("uuid", "")

    if not file_uuid:
        return "Error: No file UUID provided in the URL. Use ?uuid=your-file-uuid"

    # Check in the converted folder first
    converted_file_path = os.path.join(CONVERTED_FOLDER, f"{file_uuid}.mp3")
    if os.path.exists(converted_file_path):
        return f"File found: {file_uuid}.mp3"

    # If not in converted, check in the uploads folder
    for filename in os.listdir(UPLOAD_FOLDER):
        if filename.startswith(file_uuid):
            return f"File found: {filename}"

    return f"Error: No file found with UUID {file_uuid}"


with gr.Blocks() as status_app:
    gr.Markdown("# File Status Checker")

    status_output = gr.Markdown("Click 'Check Status' to see the result.")
    check_button = gr.Button("Check Status")

    check_button.click(fn=check_file_status, outputs=status_output)

if __name__ == "__main__":
    status_app.launch(
        server_name="127.0.0.1", server_port=7862, root_path="/long_v3/status"
    )
