from moviepy.editor import VideoFileClip, AudioFileClip
import os


def convert_to_mp3_16khz(input_path, base_path="converted"):
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

    try:
        # Determine if the input is a video or audio file
        _, ext = os.path.splitext(input_path)
        is_video = ext.lower() in [".mp4", ".avi", ".mov", ".flv", ".wmv"]

        # Load the file
        if is_video:
            clip = VideoFileClip(input_path)
            audio = clip.audio
        else:
            audio = AudioFileClip(input_path)

        # Write the audio to an MP3 file with 16000 Hz sample rate
        audio.write_audiofile(output_path, fps=16000)

        # Close the clips to free up system resources
        audio.close()
        if is_video:
            clip.close()

        print(f"Successfully converted {input_path} to MP3 (16000 Hz)")
        print(f"Saved as: {output_path}")
        return output_path

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None