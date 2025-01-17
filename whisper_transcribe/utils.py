from moviepy.editor import VideoFileClip, AudioFileClip, afx
import os
import shutil
import gradio as gr
import pysubs2
import os
import tempfile
from sanitize_filename import sanitize
from pydub import AudioSegment, effects

UPLOAD_BASE_FOLDER = "data"
CONVERTED_FOLDER = "converted"
ERROR_FOLDER = "conv_error"
BASE_URL = "https://stt4sg.fhnw.ch"  # Replace with your actual base URL
ALLOWED_EXTENSIONS = {
    ".mp3",
    ".wav",
    ".m4a",
    ".aac",
    ".flac",
    ".ogg",
    ".wma",
    ".webm",
    ".mp4",
    ".mkv",
}
# Create the paths
os.makedirs(UPLOAD_BASE_FOLDER, exist_ok=True)


def save_uploaded_file(file_path):
    if file_path is None:
        raise gr.Error(
            "No file available. Please select a file or wait for the upload to finish."
        )

    # Generate a file_name for the file
    file_name = sanitize(os.path.basename(file_path.name.split(".")[0])).replace(" ", "_")

    # Get the file extension
    _, file_extension = os.path.splitext(file_path.name)

    # Create the new filename with file_name
    new_filename = f"{file_name}{file_extension}"

    # Save the file
    original_path = os.path.join(UPLOAD_BASE_FOLDER, new_filename)
    shutil.copy(file_path.name, original_path)
    conversion_result = convert_to_mp3_16khz(original_path)
    os.remove(original_path)
    return conversion_result


def count_files_in_queue(
    folder_path=None
):
    if folder_path is None:
        folder_path = os.path.join(UPLOAD_BASE_FOLDER, CONVERTED_FOLDER)
    os.makedirs(folder_path, exist_ok=True)
    files = os.listdir(folder_path)
    return len(files)


def handle_upload(file_path):
    if file_path is None:
        raise gr.Error(
            "No file available. Please select a file or wait for the upload to finish."
        )
    # Get the file extension and validate it
    filename = file_path.name
    file_ext = os.path.splitext(filename)[1].lower()

    if file_ext not in ALLOWED_EXTENSIONS:
        raise gr.Error(
            f"Unsupported file format '{file_ext}'. Please upload an audio file in one of the following formats: "
            f"{', '.join(ALLOWED_EXTENSIONS)}"
        )
    try:
        file_name = save_uploaded_file(file_path)
        status_url = f"{BASE_URL}/long_v3/status?uuid={file_name}"
        return "**✅ File uploaded and converted successfully!** [Check transcription status here]({})".format(status_url)

    except Exception as e:
        # Log the exception details if needed
        # Optionally, log the exception here
        print(f"Error during conversion: {e}")

        os.makedirs(os.path.join(UPLOAD_BASE_FOLDER, ERROR_FOLDER), exist_ok=True)
        shutil.move(
            file_path, os.path.join(UPLOAD_BASE_FOLDER, ERROR_FOLDER, file_path)
        )
        raise gr.Error(f"An error occurred while processing your file: {e}")


def extract_audio(input_path):
    try:
        # Attempt to load as a video and extract audio
        clip = VideoFileClip(input_path)
        if clip.audio is not None:
            return clip.audio
    except Exception:
        pass  # Not a video or no audio stream
    
    try:
        # Attempt to load as an audio file
        audio = AudioFileClip(input_path)
        return audio
    except Exception:
        raise ValueError("File does not contain audio or is unsupported.")

def convert_to_mp3_16khz(input_path, base_path=CONVERTED_FOLDER):
    """
    Convert a video or audio file to MP3 format with a sample rate of 16000 Hz.
    Save the converted file in a 'converted' subfolder.

    :param input_path: Path to the input video or audio file
    :param output_path: Path to the output MP3 file. If None, it will be in a 'converted' subfolder with the same name as input but with .mp3 extension
    :return: Path to the output MP3 file
    """
    # Create a 'converted' subfolder in the same directory as the input file
    input_dir = os.path.dirname(input_path)
    converted_dir = os.path.join(input_dir, base_path)
    os.makedirs(converted_dir, exist_ok=True)

    # Generate the output filename
    input_filename = os.path.basename(input_path)
    output_filename = os.path.splitext(input_filename)[0] + ".mp3"

    # Create the full output path
    output_path = os.path.join(converted_dir, output_filename)

    # Create the lock file path
    lock_path = f"{output_path}.lock"

    # Extract audio from file
    audio = extract_audio(input_path)

    # Create lock file
    with open(lock_path, "w") as lock_file:
        lock_file.write("Conversion in progress...")

    # Write the audio to an MP3 file with 16000 Hz sample rate
    audio.write_audiofile(output_path, fps=16000, bitrate="128k")
    audio.close()

    # Normalize audio
    audio = AudioSegment.from_file(output_path)
    normalized_audio = effects.normalize(audio)
    normalized_audio.export(output_path, format="mp3")

    print(f"Successfully converted {input_path} to MP3 (16000 Hz)")
    print(f"Saved as: {output_path}")

    # Remove lock file
    os.remove(lock_path)

    return output_path


def convert_srt_to_format(srt_path, format):
    try:
        subs = pysubs2.load(srt_path)
        if format == "txt":
            content = "\n".join([line.text for line in subs])
        elif format in ["csv", "tsv"]:
            separator = "," if format == "csv" else "\t"
            content = f"Start{separator}End{separator}Text\n"
            for sub in subs:
                content += f"{sub.start}{separator}{sub.end}{separator}{sub.text}\n"
        else:  # Default to SRT
            content = subs.to_string("srt")

        return content
    except Exception as e:
        return f"Error converting file: {str(e)}"


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
