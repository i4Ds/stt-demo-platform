import os
import csv
from datetime import datetime
from collections import defaultdict

FOLDER_PATH = "/srv/stt-demo-platform/whisper_transcribe/data/transcribed"


def get_file_stats(folder_path):
    file_stats = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
            file_stats.append({"filename": filename, "creation_date": mod_date})
    return file_stats


def analyze_file_stats(file_stats):
    date_counts = defaultdict(int)
    extensions = defaultdict(int)

    for stat in file_stats:
        date_counts[stat["creation_date"]] += 1
        _, ext = os.path.splitext(stat["filename"])
        extensions[ext.lower()] += 1

    return date_counts, extensions


def generate_summary(file_stats, date_counts, extensions):
    summary = "Folder Analysis Summary:\n\n"
    summary += f"Total number of files: {len(file_stats)}\n"

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
    for date, count in sorted(date_counts.items()):
        summary += f"{date}: {count} files\n"

    return summary


def main():
    output_folder = os.path.dirname(os.path.abspath(__file__))

    file_stats = get_file_stats(FOLDER_PATH)

    date_counts, extensions = analyze_file_stats(file_stats)
    summary = generate_summary(file_stats, date_counts, extensions)

    with open(os.path.join(output_folder, "summary_report.txt"), "w") as f:
        f.write(summary)
    print(
        f"Summary report saved to: {os.path.join(output_folder, 'summary_report.txt')}"
    )


if __name__ == "__main__":
    main()
