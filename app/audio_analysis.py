import os
import numpy as np
import librosa
import matplotlib.pyplot as plt
from scipy import signal
import io
import base64
import uuid
from flask import current_app

def analyze_audio_file(file_path):
    """
    Perform audio forgery detection on the provided WAV file
    using background noise analysis.
    
    Args:
        file_path: Path to the WAV file
        
    Returns:
        result: Dictionary containing analysis results
        plots: Dictionary containing base64-encoded plots
    """
    # Load the audio file
    try:
        y, sr = librosa.load(file_path, sr=None, mono=True)
    except Exception as e:
        return {"error": f"Error loading audio file: {str(e)}"}, {}
    
    # Results dictionary
    result = {
        "duration": librosa.get_duration(y=y, sr=sr),
        "sample_rate": sr,
        "forgery_detected": False,
        "confidence": 0,
        "details": []
    }
    
    # Generate plots dictionary
    plots = {}
    
    # === Waveform and Spectrogram Analysis ===
    plots["waveform"] = create_waveform_plot(y, sr)
    plots["spectrogram"] = create_spectrogram_plot(y, sr)
    
    # === Background Noise Analysis ===
    # Extract background noise by applying high-pass filter
    # (most forgeries affect high frequency components)
    noise = extract_background_noise(y, sr)
    plots["noise_waveform"] = create_waveform_plot(noise, sr, title="Background Noise")
    
    # === ENF (Electrical Network Frequency) Analysis ===
    # Look for inconsistencies in the 50/60 Hz power line hum
    enf_result = detect_enf_inconsistencies(y, sr)
    result["details"].append(enf_result["detail"])
    if enf_result["suspicious"]:
        result["forgery_detected"] = True
        result["confidence"] = max(result["confidence"], enf_result["confidence"])
    
    # === Spectral Discontinuity Analysis ===
    # Look for sudden changes in the spectrum that might indicate splicing
    splice_result = detect_spectral_discontinuities(y, sr)
    plots["discontinuity"] = splice_result["plot"]
    result["details"].append(splice_result["detail"])
    if splice_result["suspicious"]:
        result["forgery_detected"] = True
        result["confidence"] = max(result["confidence"], splice_result["confidence"])
    
    # === Noise Level Consistency Analysis ===
    noise_result = analyze_noise_consistency(noise, sr)
    plots["noise_consistency"] = noise_result["plot"]
    result["details"].append(noise_result["detail"])
    if noise_result["suspicious"]:
        result["forgery_detected"] = True
        result["confidence"] = max(result["confidence"], noise_result["confidence"])
    
    # Format the confidence as a percentage
    result["confidence"] = int(result["confidence"] * 100)
    
    return result, plots

def extract_background_noise(y, sr):
    """Extract background noise from audio signal using a high-pass filter"""
    # High-pass filter to isolate background noise (above 5000 Hz)
    b, a = signal.butter(5, 5000/(sr/2), 'highpass')
    noise = signal.filtfilt(b, a, y)
    return noise

def detect_enf_inconsistencies(y, sr):
    """Detect inconsistencies in the Electrical Network Frequency (50/60 Hz)"""
    # Extract ENF
    window_size = int(sr * 2)  # 2-second windows
    hop_length = int(window_size / 2)
    
    enf_values = []
    suspicious = False
    confidence = 0
    
    # For real ENF analysis, we'd use more sophisticated methods
    # This is a simplified approach for demonstration
    for i in range(0, len(y) - window_size, hop_length):
        window = y[i:i+window_size]
        spectrum = np.abs(np.fft.rfft(window))
        freqs = np.fft.rfftfreq(window_size, 1/sr)
        
        # Look for energy around 50-60 Hz
        mask = (freqs >= 45) & (freqs <= 65)
        if any(mask):
            enf_power = np.mean(spectrum[mask])
            enf_values.append(enf_power)
    
    if len(enf_values) > 1:
        # Calculate variance in ENF power
        enf_variance = np.var(enf_values)
        
        # High variance might indicate tampering
        if enf_variance > np.mean(enf_values) * 0.5:
            suspicious = True
            confidence = min(0.7, enf_variance / (np.mean(enf_values) * 2))
    
    return {
        "suspicious": suspicious,
        "confidence": confidence,
        "detail": f"ENF Analysis: {'Inconsistencies detected' if suspicious else 'No significant inconsistencies'} in power line frequency components."
    }

def detect_spectral_discontinuities(y, sr):
    """Detect abrupt spectral changes that might indicate splicing"""
    # Calculate MFCC (Mel-frequency cepstral coefficients)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=512)
    
    # Calculate frame-to-frame differences
    mfcc_delta = np.diff(mfccs, axis=1)
    mfcc_delta_norm = np.linalg.norm(mfcc_delta, axis=0)
    
    # Find potential splicing points (high delta)
    threshold = np.mean(mfcc_delta_norm) + 2 * np.std(mfcc_delta_norm)
    potential_splices = np.where(mfcc_delta_norm > threshold)[0]
    
    suspicious = len(potential_splices) > 0
    confidence = min(0.8, len(potential_splices) / 10) if suspicious else 0
    
    # Create plot
    plt.figure(figsize=(10, 4))
    plt.plot(mfcc_delta_norm)
    plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
    for splice in potential_splices:
        plt.axvline(x=splice, color='g', alpha=0.5)
    plt.title('Spectral Discontinuity Analysis')
    plt.xlabel('Frame')
    plt.ylabel('MFCC Delta Norm')
    plt.legend()
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return {
        "suspicious": suspicious,
        "confidence": confidence,
        "detail": f"Spectral Discontinuity Analysis: {'Potential splicing points detected' if suspicious else 'No significant discontinuities found'}.",
        "plot": plot_data
    }

def analyze_noise_consistency(noise, sr):
    """Analyze the consistency of background noise levels"""
    # Split into segments
    segment_length = int(sr * 1)  # 1 second segments
    hop_length = int(segment_length / 2)  # 50% overlap
    
    noise_levels = []
    timestamps = []
    
    for i in range(0, len(noise) - segment_length, hop_length):
        segment = noise[i:i+segment_length]
        # Calculate RMS energy
        rms = np.sqrt(np.mean(segment**2))
        noise_levels.append(rms)
        timestamps.append(i / sr)
    
    # Check for significant variations in noise level
    noise_mean = np.mean(noise_levels)
    noise_std = np.std(noise_levels)
    threshold = noise_mean + 2 * noise_std
    
    outliers = np.where(noise_levels > threshold)[0]
    suspicious = len(outliers) > 0
    confidence = min(0.75, len(outliers) / 10) if suspicious else 0
    
    # Create plot
    plt.figure(figsize=(10, 4))
    plt.plot(timestamps, noise_levels)
    plt.axhline(y=threshold, color='r', linestyle='--', label='Threshold')
    for outlier in outliers:
        plt.axvline(x=timestamps[outlier], color='g', alpha=0.5)
    plt.title('Background Noise Consistency Analysis')
    plt.xlabel('Time (s)')
    plt.ylabel('Noise Level (RMS)')
    plt.legend()
    plt.tight_layout()
    
    # Convert plot to base64 string
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return {
        "suspicious": suspicious,
        "confidence": confidence,
        "detail": f"Noise Consistency Analysis: {'Inconsistent noise levels detected' if suspicious else 'Background noise is consistent throughout the recording'}.",
        "plot": plot_data
    }

def create_waveform_plot(y, sr, title="Audio Waveform"):
    """Create a waveform plot and return as base64-encoded PNG"""
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title(title)
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return plot_data

def create_spectrogram_plot(y, sr):
    """Create a spectrogram plot and return as base64-encoded PNG"""
    plt.figure(figsize=(10, 4))
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    librosa.display.specshow(D, sr=sr, x_axis='time', y_axis='log')
    plt.colorbar(format='%+2.0f dB')
    plt.title('Spectrogram')
    plt.tight_layout()
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()
    
    return plot_data
