# Auto-Organizer: A Python CLI for Decluttering Directories

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
[![GitHub last commit](https://img.shields.io/github/last-commit/Mayank230604/auto-organizer?color=orange)](https://github.com/Mayank230604/auto-organizer/commits/main)

## 🌟 Project Overview

**Auto-Organizer** is a powerful and easy-to-use command-line interface (CLI) tool written in Python. It's designed to help you quickly clean up messy directories (like your `Downloads` folder) by automatically sorting files into organized subdirectories based on their file type. No more hunting for that one PDF amidst hundreds of images and videos!

This project was built to demonstrate fundamental Python programming skills, file system interaction, and command-line argument parsing.

## ✨ Features

* **Targeted Cleaning**: Organize any specified directory by passing its path as a command-line argument.
* **Smart Categorization**: Files are intelligently sorted into predefined categories (e.g., Images, Documents, Videos, Audio, Archives, Code, Executables, Other) based on their file extensions.
* **Automatic Folder Creation**: Automatically creates necessary category folders (e.g., `Images`, `Documents`) if they don't already exist in the target directory.
* **Safe File Handling**: Gracefully moves files to their new locations.
* **Duplicate File Renaming**: Handles cases where a file with the same name already exists in the destination folder by appending a counter (e.g., `report.pdf` becomes `report_1.pdf`).
* **Summary Report**: Provides a detailed summary after execution, showing how many files of each type were moved.

## 🚀 Getting Started

Follow these steps to get Auto-Organizer up and running on your local machine.

### Prerequisites

* Python 3.6 or higher (tested with Python 3.9+)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Mayank230604/auto-organizer.git](https://github.com/Mayank230604/auto-organizer.git)
    cd auto-organizer
    ```

2.  **No extra dependencies are required!** This project uses only Python's built-in `os`, `shutil`, and `argparse` libraries.

## 💡 Usage

To run the Auto-Organizer, simply execute the `organizer.py` script and provide the path to the directory you wish to clean as an argument.

**Basic Usage:**

```bash
python organizer.py /path/to/your/target-directory
