# Import the 'os' module to interact with the operating system (e.g., check files, open them)
import os

# Import 'VideosSearch' from the third-party library to search YouTube programmatically
from youtubesearchpython import VideosSearch

# Import 'yt-dlp' library to download media content from the internet
import yt_dlp

# Prompt the user to type in the name of the song they want to search for
name = input("Enter your song: ")

# Check if the user entered an empty string or just whitespace after stripping spaces
if len(name.strip()) < 1:
    # Print an error message if the input is empty
    print("Sorry, your song is empty")
    # Stop the script execution immediately
    exit()

# Inform the user that the search process has started
print("Searching YouTube...")

# Initialize the YouTube search with the user's query, limiting the results to top 1
videos_search = VideosSearch(name, limit=1)

# Extract the search results dictionary and get the list under 'result', defaulting to an empty list if nothing returns
results = videos_search.result().get("result", [])

# Check if the results list is empty (meaning no videos matched the search query)
if not results:
    # Inform the user that no matches were found
    print("No results found.")
    # Exit the program
    exit()

# Extract the YouTube video URL from the first result dictionary
video_url = results[0]["link"]

# Extract the title of the video from the first result dictionary
video_title = results[0]["title"]

# Extract the unique video ID from the first result dictionary
video_id = results[0]["id"]

# Look for common audio extensions using the unique video ID to see if it was previously downloaded
existing_file = None
for ext in ['webm', 'm4a', 'mp3', 'opus']:
    possible_path = f'song_{video_id}.{ext}'
    # Check if this file name already exists in the folder
    if os.path.exists(possible_path):
        existing_file = possible_path
        break

# Use a try-except block to safely catch and handle any download or playback errors
try:
    # Check if we found an already downloaded file for this song
    if existing_file:
        print(f"Found already downloaded song: {video_title}")
        filename = existing_file
    else:
        # If it doesn't exist locally, download it fresh from YouTube
        print(f"Downloading: {video_title}...")

        # Configure download options for yt-dlp to grab the best available audio format
        ydl_opts = {
            'format': 'bestaudio',  # Select the highest quality audio stream available
            'outtmpl': f'song_{video_id}.%(ext)s',  # Set a unique filename using the video ID
            'quiet': True,  # Suppress verbose terminal output logs from yt-dlp
            'overwrites': True  # Force overwrite if needed
        }

        # Initialize the yt-dlp downloader context manager with our configured options
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract the video stream info and download the file to the local directory
            info = ydl.extract_info(video_url, download=True)

            # Get the final generated filename with its proper extension
            filename = ydl.prepare_filename(info)

    # Convert the relative filename into an absolute file path on the computer
    file_path = os.path.abspath(filename)

    # Inform the user that the system default media player is about to launch
    print(f"Opening with Windows Media Player...")

    # Tell the Windows operating system to open the audio file using its default application association
    os.startfile(file_path)

# Catch any unexpected errors that occur during the process
except Exception as e:
    # Print the specific error message
    print(f"An error occurred: {e}")

    # Provide a fallback clickable text link so the user can still open the song manually in a browser
    print(f"Direct video link to open manually: {video_url}")

