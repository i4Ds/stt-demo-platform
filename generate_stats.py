import os
import csv
from datetime import datetime
from collections import defaultdict

from mutagen.mp3 import MP3


# Fixed fallback bitrate (matches convert_and_normalize_mp3_16khz target)
BITRATE_BPS = 128_000

FOLDER_PATH = "/srv/stt-demo-platform/whisper_transcribe/data/processed"


def estimate_duration_seconds(file_size_bytes: int, bitrate_bps: int = BITRATE_BPS):
    """Estimate duration from file size assuming constant bitrate MP3."""

    if bitrate_bps <= 0:
        raise ValueError("bitrate_bps must be positive")
    return (file_size_bytes * 8) / bitrate_bps


def format_duration(seconds: float) -> str:
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours:d}h {minutes:02d}m {secs:02d}s"
    if minutes:
        return f"{minutes:d}m {secs:02d}s"
    return f"{secs:d}s"


def get_mp3_duration_and_bitrate(path: str):
    """Return (duration_sec, bitrate_bps) using mutagen, or (None, None)."""

    if MP3 is None:
        return None, None
    try:
        info = MP3(path).info
        duration = getattr(info, "length", None)
        bitrate = getattr(info, "bitrate", None)
        return duration, bitrate
    except Exception:
        return None, None


def get_file_stats(folder_path):
    file_stats = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
            file_size = os.path.getsize(file_path)
            ext = os.path.splitext(filename)[1].lower()
            duration_sec = None
            bitrate_bps = BITRATE_BPS

            if ext == ".mp3":
                mutagen_duration, mutagen_bitrate = get_mp3_duration_and_bitrate(
                    file_path
                )
                if mutagen_bitrate:
                    bitrate_bps = mutagen_bitrate
                if mutagen_duration:
                    duration_sec = mutagen_duration

            if duration_sec is None:
                duration_sec = estimate_duration_seconds(file_size, bitrate_bps)

            file_stats.append(
                {
                    "filename": filename,
                    "creation_date": mod_date,
                    "file_size": file_size,
                    "duration_sec": duration_sec,
                }
            )
    return file_stats


def analyze_file_stats(file_stats):
    date_counts = defaultdict(int)
    extensions = defaultdict(int)
    files_by_date = defaultdict(list)
    total_size = 0
    total_duration = 0.0
    for stat in file_stats:
        date_counts[stat["creation_date"]] += 1
        _, ext = os.path.splitext(stat["filename"])
        extensions[ext.lower()] += 1
        files_by_date[stat["creation_date"]].append(
            (
                stat["filename"],
                stat["file_size"],
                stat["duration_sec"],
            )
        )
        total_size += stat["file_size"]
        total_duration += stat["duration_sec"]
    return date_counts, extensions, files_by_date, total_size, total_duration


def generate_summary(
    file_stats, date_counts, extensions, files_by_date, total_size, total_duration
):
    summary = "Folder Analysis Summary:\n\n"
    summary += f"Total number of files: {len(file_stats)}\n"
    summary += f"Total size of files: {total_size / (1024 * 1024):.2f} MB\n"
    summary += (
        "Estimated total audio duration: "
        f"{format_duration(total_duration)} (mutagen MP3 length when available, else {BITRATE_BPS/1000:.0f} kbps)\n"
    )
    if date_counts:
        min_date = min(date_counts.keys())
        max_date = max(date_counts.keys())
        summary += f"Date range: {min_date} to {max_date}\n"
        most_files_date = max(date_counts, key=date_counts.get)
        summary += f"Day with most files created: {most_files_date} ({date_counts[most_files_date]} files)\n"
    if extensions:
        most_common_ext = max(extensions, key=extensions.get)
        summary += f"Most common file extension: {most_common_ext} ({extensions[most_common_ext]} files)\n"

    summary += "\nFiles created per day:\n"
    for date, files in sorted(files_by_date.items()):
        daily_duration = sum(f[2] for f in files)
        summary += (
            f"{date}: {len(files)} files" f" (est. {format_duration(daily_duration)})\n"
        )
        summary += "Files:\n"
        for file, size, duration in files:
            summary += (
                f"  - {file} ({size / (1024 * 1024):.2f} MB, "
                f"~{format_duration(duration)})\n"
            )
    return summary


def main():
    output_folder = os.path.dirname(os.path.abspath(__file__))
    file_stats = get_file_stats(FOLDER_PATH)
    (
        date_counts,
        extensions,
        files_by_date,
        total_size,
        total_duration,
    ) = analyze_file_stats(file_stats)
    summary = generate_summary(
        file_stats,
        date_counts,
        extensions,
        files_by_date,
        total_size,
        total_duration,
    )
    with open(os.path.join(output_folder, "summary_report.txt"), "w") as f:
        f.write(summary)
    print(
        f"Summary report saved to: {os.path.join(output_folder, 'summary_report.txt')}"
    )


if __name__ == "__main__":
    main()
