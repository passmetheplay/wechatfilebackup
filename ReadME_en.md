[English version](https://github.com/passmetheplay/wechatfilebackup/blob/main/ReadME_en.md)
# MacOS - WeChat File Search and Migration Tool

## Introduction

This tool is designed to help users efficiently search and migrate files stored in the WeChat application on MacOS. It offers an easy way to find, filter, and migrate videos, images, and voice files in WeChat, especially suitable for users who need to organize a large number of files in WeChat chat history.
``` Note: Currently only supports MacOS ```

Here is an introduction video:

https://github.com/passmetheplay/wechatfilebackup/assets/143151096/d4b1e976-6433-47fb-b287-3b2f5b9b5802


## Problems Solved

- **File Search**: Automatically or manually search for WeChat files on Mac, including videos, images, and voice files.
- **File Migration**: Batch migrate selected files to a specified folder for easy file management and backup.
- **Format Conversion**: Convert WeChat's `.silk` voice files to the more common `.mp3` format.
- **Selective Deletion**: Option to delete original files after migration to help free up storage space.

## User Guide

### Installation

Please download the latest version of the application from the GitHub page, install the Python environment, and then run the `main.py` file. A MacOS application version will be released in the future.

### Usage Steps

1. **Select Search Directory**:
    - The program attempts to automatically locate the default storage directory of WeChat.
    - If needed, you can manually select another directory by clicking the “Select Folder” button.
2. **Start Search**:
    - Click the “Start Search” button to search for files in the selected directory.
    - After the search is complete, the program will display the quantity of each type of file and list all found files.
3. **File Migration Settings**:
    - Select the files you wish to migrate from the search results.
    - Click the “Select Migration Target Folder” button to specify the destination for file migration.
    - Download and install [silk-v3-decoder](https://github.com/kn007/silk-v3-decoder)
    - To convert `.silk` format voice files to `.wav` format, check the relevant option and set the silk-v3-decoder directory.
    - To delete original files after migration, check the “Delete Source Files” option.
4. **Start Migration**:
    - Click the “Start Migration” button, and the selected files will begin migrating to your specified target folder.
    - After completion, the program will display the number of migrated files and the number of converted voice files.
5. **Voice Conversion Explanation**:
   - The conversion of voice files is from silk format to mp3 format playable by common players, using silk-v3-decoder. If silk-v3-decoder also fails to convert, [FFmpeg](https://ffmpeg.org/about.html) is used. For FFmpeg installation, please follow these steps:
     1. Install Homebrew:
        Open the MacOS terminal. Enter the following command to install Homebrew:
       `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
     2. Install FFmpeg:
        Once Homebrew is installed, just run the following command in the terminal to install FFmpeg:
        `brew install ffmpeg`
     3. During the installation, you may be prompted to enter a password. Enter your Mac account password.
     4. After installation, you can check if it's installed successfully by running `brew install ffmpeg`.

### Help and Support

If you have any questions or need technical support, please refer to the help section in the application or submit issues on the GitHub page.
