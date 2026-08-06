# YouTube Audio Downloader

A simple command-line tool that searches YouTube for a song by name, downloads the best available audio track, and opens it in your system's default media player. Previously downloaded songs are detected and reused instead of being re-downloaded.

## Features

- Search YouTube by song/artist name and grab the top result
- Download the best available audio stream using `yt-dlp`
- Skip re-downloading if the song was already fetched before
- Automatically open the downloaded file in your default media player
- Falls back to printing a direct video link if something goes wrong

## Requirements

- Python 3.8+
- Windows (the script uses `os.startfile`, a Windows-only function, to launch the media player)
- The following Python packages:
  - `yt-dlp`
  - `youtube-search-python`

## Installation

1. Make sure Python 3 is installed and available on your PATH.
2. Install the required packages:

   ```bash
   pip install yt-dlp youtube-search-python
   ```

3. Save the script (e.g. as `youtube_audio_downloader.py`) in a folder where you're okay with audio files being saved.

## Usage

Run the script from the command line:

```bash
python youtube_audio_downloader.py
```

You'll be prompted to enter a song name:

```
Enter your song: bohemian rhapsody
```

The script will:

1. Search YouTube and pick the top matching video.
2. Check whether that song was already downloaded (by video ID).
3. Download it if needed, using the format `song_<video_id>.<ext>`.
4. Open the resulting audio file with your default media player.

## Output Files

Downloaded audio is saved in the same directory the script is run from, using the naming pattern:

```
song_<video_id>.<extension>
```

The extension depends on whatever format `yt-dlp` selects as "best audio" (commonly `.webm`, `.m4a`, `.mp3`, or `.opus`).

## Notes & Limitations

- **Windows only**: `os.startfile()` is not available on macOS or Linux. On those platforms you'd need to replace it with something like `subprocess.run(["open", file_path])` (macOS) or `subprocess.run(["xdg-open", file_path])` (Linux).
- **No format conversion**: The script downloads whatever "best audio" format YouTube provides — it does not convert to MP3. Add `postprocessors` to the `yt_dlp` options if you need a specific format.
- **Single result only**: The script only looks at the top search result, so it may occasionally grab the wrong video for ambiguous song titles.
- **Terms of Service**: Downloading content from YouTube may violate YouTube's Terms of Service depending on your use case and jurisdiction. Use this tool responsibly and only for content you have the right to download (e.g. your own uploads or content explicitly licensed for download).

## Troubleshooting

| Issue | Possible Cause |
|---|---|
| `No results found.` | The search query didn't match any videos — try a different or more specific name. |
| `An error occurred: ...` | Network issue, YouTube API changes, or `yt-dlp` needs updating (`pip install -U yt-dlp`). |
| Media player doesn't open | Confirm the downloaded file's extension has a default application associated with it on Windows. |
