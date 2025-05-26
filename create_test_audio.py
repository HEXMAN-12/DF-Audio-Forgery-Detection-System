import sys
import os
import numpy as np
import librosa
from scipy.io import wavfile

def create_test_audio(filename, duration=5, sample_rate=44100):
    """
    Create a test WAV file with a simple sine wave and some noise
    
    Args:
        filename: Output WAV file path
        duration: Duration in seconds
        sample_rate: Sample rate in Hz
    """
    print(f"Creating test audio file: {filename}")
    
    # Generate a time array
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Generate a 440 Hz sine wave
    tone = 0.5 * np.sin(2 * np.pi * 440 * t)
    
    # Add some background noise
    noise = 0.1 * np.random.normal(0, 1, len(t))
    
    # Combine the tone and noise
    audio = tone + noise
    
    # Normalize
    audio = audio / np.max(np.abs(audio))
    
    # Convert to int16
    audio_int16 = (audio * 32767).astype(np.int16)
    
    # Save as WAV file
    wavfile.write(filename, sample_rate, audio_int16)
    
    print(f"Test audio file created: {filename}")
    return filename

def create_tampered_audio(filename, original_file, sample_rate=44100):
    """
    Create a tampered version of an audio file by splicing two segments
    
    Args:
        filename: Output WAV file path
        original_file: Original WAV file path
        sample_rate: Sample rate in Hz
    """
    print(f"Creating tampered audio file: {filename}")
    
    # Load the original audio
    y, sr = librosa.load(original_file, sr=sample_rate, mono=True)
    
    # Split the audio into two segments
    segment1 = y[:len(y)//2]
    segment2 = y[len(y)//2:]
    
    # Create a new segment with different noise characteristics
    t = np.linspace(0, len(segment2)/sample_rate, len(segment2), False)
    tone = 0.5 * np.sin(2 * np.pi * 440 * t)
    noise = 0.2 * np.random.normal(0, 1, len(segment2))  # Different noise level
    new_segment = tone + noise
    new_segment = new_segment / np.max(np.abs(new_segment))
    
    # Splice the segments together
    tampered = np.concatenate((segment1, new_segment))
    
    # Normalize
    tampered = tampered / np.max(np.abs(tampered))
    
    # Convert to int16
    tampered_int16 = (tampered * 32767).astype(np.int16)
    
    # Save as WAV file
    wavfile.write(filename, sample_rate, tampered_int16)
    
    print(f"Tampered audio file created: {filename}")
    return filename

def main():
    # Create test directory if it doesn't exist
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_audio")
    os.makedirs(test_dir, exist_ok=True)
    
    # Create a clean test audio file
    clean_file = os.path.join(test_dir, "clean_audio.wav")
    create_test_audio(clean_file)
    
    # Create a tampered version
    tampered_file = os.path.join(test_dir, "tampered_audio.wav")
    create_tampered_audio(tampered_file, clean_file)
    
    print("\nTest files created successfully!")
    print(f"Clean audio: {clean_file}")
    print(f"Tampered audio: {tampered_file}")
    print("\nYou can use these files to test the audio forgery detection system.")

if __name__ == "__main__":
    main()
