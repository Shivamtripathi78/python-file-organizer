from pathlib import Path
import shutil


# File extensions and their destination folders.
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".ppt", ".pptx", ".xlsx", ".csv"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".html", ".css"],
}


def get_category(file_path):
    """Return the category for a file based on its extension."""
    extension = file_path.suffix.lower()

    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category

    return "Others"


def get_unique_path(destination):
    """Avoid overwriting a file with the same name."""
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_destination = destination.with_name(
            f"{destination.stem}_{counter}{destination.suffix}"
        )

        if not new_destination.exists():
            return new_destination

        counter += 1


def organize_files(folder_path):
    """Organize files in the selected folder into category folders."""
    folder = Path(folder_path).expanduser()

    if not folder.exists() or not folder.is_dir():
        print("Error: The specified folder does not exist.")
        return

    # Only organize files directly inside the selected folder.
    files = [
        item for item in folder.iterdir()
        if item.is_file() and item.name != Path(__file__).name
    ]

    if not files:
        print("No files found to organize.")
        return

    moved_count = 0

    for file_path in files:
        category = get_category(file_path)
        destination_folder = folder / category
        destination_folder.mkdir(exist_ok=True)

        destination = get_unique_path(destination_folder / file_path.name)

        try:
            shutil.move(str(file_path), str(destination))
            print(f"Moved: {file_path.name} -> {category}/")
            moved_count += 1

        except OSError as error:
            print(f"Could not move {file_path.name}: {error}")

    print(f"\nOrganization complete! Files moved: {moved_count}")


def main():
    print("=" * 45)
    print("          PYTHON FILE ORGANIZER")
    print("=" * 45)

    folder_path = input(
        "\nEnter the folder path to organize: "
    ).strip().strip('"')

    confirm = input(
        f"\nOrganize files in '{folder_path}'? (y/n): "
    ).strip().lower()

    if confirm != "y":
        print("Operation cancelled.")
        return

    organize_files(folder_path)


if __name__ == "__main__":
    main()