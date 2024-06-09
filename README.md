# YouTube to MP3 Converter

## Overview
The YouTube to MP3 Converter is a simple tool that allows users to convert YouTube videos into MP3 audio files. This can be useful for listening to your favorite music, podcasts, or any other audio content offline, without needing to stream the video each time.

## Features
- **Easy Conversion**: Convert YouTube videos to MP3 format with a few clicks.
- **High-Quality Audio**: Choose the audio quality for the MP3 file.
- **Batch Processing**: Convert multiple YouTube videos simultaneously.
- **Metadata Support**: Automatically fetches and includes metadata such as artist, album, and title.
- **Cross-Platform**: Available on Windows, macOS, and Linux.
- **User-Friendly Interface**: Simple and intuitive UI for a seamless experience.

## Requirements
- Python 3.7 or higher
- `pytube` library for downloading YouTube videos
- `pydub` library for converting video to audio
- `ffmpeg` installed on your system

## Installation

1. **Install Python**: Ensure Python 3.7 or higher is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **Install Required Libraries**:
    ```sh
    pip install pytube pydub
    ```

3. **Install FFmpeg**:
    - **Windows**: Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add it to your system's PATH.
    - **macOS**: Use Homebrew:
        ```sh
        brew install ffmpeg
        ```
    - **Linux**: Install via package manager:
        ```sh
        sudo apt-get install ffmpeg
        ```

## Usage

1. **Run the Converter**: Execute the script `youtube_to_mp3.py`.

2. **Input the YouTube URL**: Paste the URL of the YouTube video you want to convert.

3. **Choose Audio Quality**: Select the desired audio quality (e.g., 128kbps, 192kbps, 320kbps).

4. **Start Conversion**: Click the "Convert" button to begin the conversion process.

5. **Save MP3 File**: Once the conversion is complete, the MP3 file will be saved to your specified directory.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue to discuss what you would like to change.

## Contact
For any inquiries or support, please contact (sebuguerojanmark@gmail.com).
