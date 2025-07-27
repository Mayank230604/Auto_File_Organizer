"""
Auto-Organizer: A Command-Line Interface (CLI) tool to sort files in a specified directory.

This script scans a given directory and organizes its files into subdirectories
based on their file extensions (e.g., 'Images', 'Documents', 'Audio').
It handles creation of category folders and manages duplicate filenames.
"""

import os
import shutil
import argparse

# Define file categories. Add or remove categories/extensions as needed.
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".ppt", ".odt", ".rtf", ".md"], # Added .md
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"], # Added .m4a
    "Video": [".mp4", ".mov", ".avi", ".mkv", ".flv", ".wmv", ".webm"], # Added .webm
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso"], # Added .iso
    "Executables": [".exe", ".msi", ".dmg", ".app", ".bat", ".sh"], # Added .bat, .sh (for scripts)
    "Code": [".py", ".js", ".html", ".css", ".java", ".c", ".cpp", ".h", ".cs", ".go", ".rb", ".php", ".json", ".xml", ".yml", ".yaml"] # Expanded code types
}

def get_category(file_extension):
    """
    Determines the category of a file based on its extension.
    The extension comparison is case-insensitive.
    Returns 'Other' if no matching category is found.
    """
    ext = file_extension.lower() # Convert extension to lowercase for consistent matching
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Other" # Default category for unhandled extensions

def organize_directory(path):
    """
    Organizes files in the specified target directory into category-based subfolders.
    
    This function performs the following steps:
    1. Validates if the provided path is a directory.
    2. Creates all necessary category folders (and an 'Other' folder) within the target directory.
    3. Iterates through each item in the directory.
    4. For each file, it determines its category using `get_category`.
    5. Moves the file to its respective category folder.
    6. Handles potential filename conflicts by renaming duplicate files (e.g., file.txt -> file_1.txt).
    7. Prints a summary of moved files by category.
    """
    print(f"Starting organization in: '{path}'\n")

    # Validate if the provided path is a valid directory
    if not os.path.isdir(path):
        print(f"Error: Directory '{path}' not found or is not a directory.")
        print("Please provide a valid directory path to organize.")
        return

    # 1. Create all necessary category folders upfront
    print("Ensuring category directories exist...")
    # Compile a list of all categories, including "Other"
    all_categories_names = list(CATEGORIES.keys()) + ["Other"] 
    
    for category_name in all_categories_names:
        category_folder_path = os.path.join(path, category_name)
        # os.makedirs creates directories recursively; exist_ok=True prevents errors if it already exists
        os.makedirs(category_folder_path, exist_ok=True) 
        print(f"  - Ensured: '{os.path.basename(category_folder_path)}/'")
    print("\n")


    print("Processing files...")
    # Initialize a dictionary to track the count of files moved per category
    moved_files_count = {category: 0 for category in all_categories_names}

    # Get a list of items in the directory *before* starting to move them.
    # This prevents issues if directory contents change during iteration.
    files_to_process = [item for item in os.listdir(path) if os.path.isfile(os.path.join(path, item))]

    if not files_to_process:
        print("No files found to organize in the target directory.")
        # Print summary even if no files were found, to indicate completion
        print("\nOrganization complete!")
        print("\n--- Summary ---")
        print("  No files were moved.")
        print("---------------\n")
        return # Exit if no files to process

    for item in files_to_process:
        item_path = os.path.join(path, item)

        # Skip if the item is one of our newly created (or existing) category folders
        # This check is technically redundant since we filter for is_file above, but harmless.
        if os.path.isdir(item_path) and item in all_categories_names:
            continue 
        
        # Ensure we are only processing actual files
        if os.path.isfile(item_path):
            # os.path.splitext returns a tuple: (root, ext) e.g., ('document', '.pdf')
            base_name, file_extension = os.path.splitext(item)
            category = get_category(file_extension)
            
            # Construct the destination folder path
            destination_folder = os.path.join(path, category)
            # Construct the initial destination path for the file
            destination_file_name = item
            destination_path = os.path.join(destination_folder, destination_file_name)

            # Handle Duplicate Files: If a file with the same name exists, rename the new one
            counter = 1
            # Keep track of the original name for printing messages
            original_item_name_for_log = item 
            
            while os.path.exists(destination_path):
                # Append a counter to the base name if a duplicate exists
                destination_file_name = f"{base_name}_{counter}{file_extension}"
                destination_path = os.path.join(destination_folder, destination_file_name)
                counter += 1
            
            try:
                # Attempt to move the file
                shutil.move(item_path, destination_path)
                
                # Provide clear feedback to the user
                if original_item_name_for_log != destination_file_name:
                    print(f"  - Moved '{original_item_name_for_log}' to '{category}/{destination_file_name}' (renamed due to conflict)")
                else:
                    print(f"  - Moved '{original_item_name_for_log}' to '{category}/'")
                
                # Increment the count for the respective category
                moved_files_count[category] += 1
            except shutil.Error as se:
                # Catch specific shutil errors (e.g., permissions)
                print(f"  - Permission Error moving '{original_item_name_for_log}' to '{category}/': {se}")
            except OSError as oe:
                # Catch general OS errors (e.g., path too long, invalid characters)
                print(f"  - OS Error moving '{original_item_name_for_log}' to '{category}/': {oe}")
            except Exception as e:
                # Catch any other unexpected errors
                print(f"  - An unexpected error occurred moving '{original_item_name_for_log}': {e}")
    
    print("\nOrganization complete!")
    print("\n--- Summary ---")
    total_moved = 0
    # Sort categories alphabetically for a cleaner summary
    sorted_categories = sorted(moved_files_count.keys())
    
    for category in sorted_categories:
        count = moved_files_count[category]
        if count > 0:
            print(f"  {category}: {count} file(s) moved.")
            total_moved += count
    
    if total_moved == 0:
        print("  No files were moved from the root of the specified directory.")
    print("---------------\n")


def main():
    """
    Main function to parse command-line arguments and initiate the
    file organization process.
    """
    parser = argparse.ArgumentParser(
        description="Auto-Organizer: A Command-Line Interface (CLI) tool "
                    "to sort files in a specified directory based on their type.",
        formatter_class=argparse.RawTextHelpFormatter # Improves formatting for help message
    )
    
    # Add the required 'directory' argument
    parser.add_argument(
        "directory",
        type=str,
        help="The path to the directory you want to organize.\n"
             "Example: C:\\Users\\YourUser\\Downloads (Windows)\n"
             "         /home/youruser/Downloads (Linux/macOS)"
    )

    args = parser.parse_args()
    
    # Call the organization function with the parsed directory path
    organize_directory(args.directory)

# This ensures main() is called only when the script is executed directly
if __name__ == "__main__":
    main()