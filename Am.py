import pyttsx3
import PyPDF2
from pydub import AudioSegment
import os
from pathlib import Path

# Create audio directory if it doesn't exist
AUDIO_DIR = Path('Folder for audio')
AUDIO_DIR.mkdir(exist_ok=True)

def create_audio(file_path, output_name):
    # Initialize speaker
    speaker = pyttsx3.init()
    speaker.setProperty('rate', 150)  # Speed percent
    speaker.setProperty('volume', 0.9)  # Volume

    def process_text(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text

    # Process the text file
    text = process_text(file_path)

    # Create temporary WAV in audio folder
    temp_wav = AUDIO_DIR / 'output.wav'
    speaker.save_to_file(text, str(temp_wav))
    speaker.runAndWait()

    # Convert WAV to MP3 using pydub (requires ffmpeg)
    sound = AudioSegment.from_wav(str(temp_wav))
    mp3_path = AUDIO_DIR / f"{output_name}.mp3"
    sound.export(str(mp3_path), format="mp3")

    # Cleanup temporary WAV file
    os.remove(temp_wav)

    print(f"Audiobook creation complete: {mp3_path}")
    return str(mp3_path)

# This function can now be imported and used in other scripts
