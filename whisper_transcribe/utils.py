from moviepy.editor import VideoFileClip, AudioFileClip
import os
import uuid
import shutil
import gradio as gr
import pysubs2
import os
import tempfile

UPLOAD_FOLDER = "data"
CONVERTED_FOLDER = "converted"
ERROR_FOLDER = "conv_error"
BASE_URL = "https://stt4sg.fhnw.ch"  # Replace with your actual base URL


def save_uploaded_file(file):
    if file is None:
        return None

    # Generate a UUID for the file
    file_uuid = str(uuid.uuid4())

    # Get the file extension
    _, file_extension = os.path.splitext(file.name)

    # Create the new filename with UUID
    new_filename = f"{file_uuid}{file_extension}"

    # Save the file
    original_path = os.path.join(UPLOAD_FOLDER, new_filename)
    shutil.copy(file.name, original_path)

    conversion_result = convert_to_mp3_16khz(original_path)

    if conversion_result:
        # Optionally, remove the original file to save space
        os.remove(original_path)
        print(f"Converted and saved as MP3: {conversion_result}")
    else:
        print(f"Conversion failed. Original file retained: {original_path}")

    return file_uuid


def handle_upload(file):
    if file is None:
        raise gr.Error("No file selected. Please select a file to process.")

    file_uuid = save_uploaded_file(file)
    if file_uuid:
        status_url = f"{BASE_URL}/long_v3/status?uuid={file_uuid}"
        return f"File uploaded & converted successfully. Check the status here: [Transcription Status]({status_url})"
    else:
        raise gr.Error("Failed to upload file. Please try again.")


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

    # If no output path is specified, create one in the 'converted' folder
    input_filename = os.path.basename(input_path)
    output_filename = os.path.splitext(input_filename)[0] + ".mp3"
    output_path = os.path.join(converted_dir, output_filename)
    lock_path = os.path.join(converted_dir, output_filename + ".lock")

    try:
        # Determine if the input is a video or audio file
        _, ext = os.path.splitext(input_path)
        is_video = ext.lower() in [".mp4", ".avi", ".mov", ".flv", ".wmv"]

        # Load the file
        if is_video:
            clip = VideoFileClip(input_path)
            audio = clip.audio
            clip.close()
        else:
            audio = AudioFileClip(input_path)

        # Create lock file
        with open(lock_path, "w") as lock_file:
            lock_file.write("Conversion in progress...")

        # Write the audio to an MP3 file with 16000 Hz sample rate
        audio.write_audiofile(output_path, fps=16000, bitrate="128k")

        # Close the clips to free up system resources
        audio.close()

        print(f"Successfully converted {input_path} to MP3 (16000 Hz)")
        print(f"Saved as: {output_path}")

        # Remove lock file
        os.remove(lock_path)

        return output_path

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        os.makedirs(os.path.join(UPLOAD_FOLDER, ERROR_FOLDER), exist_ok=True)
        shutil.move(
            input_path, os.path.join(UPLOAD_FOLDER, ERROR_FOLDER, input_filename)
        )
        return None


def convert_srt_to_format(srt_path, format, include_timestamps=True):
    try:
        subs = pysubs2.load(srt_path)
        if format == "txt":
            content = (
                "\n".join([line.text for line in subs])
                if not include_timestamps
                else subs.to_string("srt")
            )
        elif format in ["csv", "tsv"]:
            separator = "," if format == "csv" else "\t"
            content = (
                f"Start{separator}End{separator}Text\n"
                if include_timestamps
                else f"Text\n"
            )
            for sub in subs:
                if include_timestamps:
                    content += f"{sub.start}{separator}{sub.end}{separator}{sub.text}\n"
                else:
                    content += f"{sub.text}\n"
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
