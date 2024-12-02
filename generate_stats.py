import os
import csv
from datetime import datetime
from collections import defaultdict

FOLDER_PATH = "/srv/stt-demo-platform/whisper_transcribe/data/processed"


def get_file_stats(folder_path):
    file_stats = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            mod_time = os.path.getmtime(file_path)
            mod_date = datetime.fromtimestamp(mod_time).strftime("%Y-%m-%d")
            file_size = os.path.getsize(file_path)
            file_stats.append(
                {
                    "filename": filename,
                    "creation_date": mod_date,
                    "file_size": file_size,
                }
            )
    return file_stats


def analyze_file_stats(file_stats):
    date_counts = defaultdict(int)
    extensions = defaultdict(int)
    files_by_date = defaultdict(list)
    total_size = 0
    for stat in file_stats:
        date_counts[stat["creation_date"]] += 1
        _, ext = os.path.splitext(stat["filename"])
        extensions[ext.lower()] += 1
        files_by_date[stat["creation_date"]].append(
            (stat["filename"], stat["file_size"])
        )
        total_size += stat["file_size"]
    return date_counts, extensions, files_by_date, total_size


def generate_summary(file_stats, date_counts, extensions, files_by_date, total_size):
    summary = "Folder Analysis Summary:\n\n"
    summary += f"Total number of files: {len(file_stats)}\n"
    summary += f"Total size of files: {total_size / (1024 * 1024):.2f} MB\n"
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
        summary += f"{date}: {len(files)} files\n"
        summary += "Files:\n"
        for file, size in files:
            summary += f"  - {file} ({size / (1024 * 1024):.2f} MB)\n"
    return summary


def main():
    output_folder = os.path.dirname(os.path.abspath(__file__))
    file_stats = get_file_stats(FOLDER_PATH)
    date_counts, extensions, files_by_date, total_size = analyze_file_stats(file_stats)
    summary = generate_summary(
        file_stats, date_counts, extensions, files_by_date, total_size
    )
    with open(os.path.join(output_folder, "summary_report.txt"), "w") as f:
        f.write(summary)
    print(
        f"Summary report saved to: {os.path.join(output_folder, 'summary_report.txt')}"
    )


if __name__ == "__main__":
    main()
