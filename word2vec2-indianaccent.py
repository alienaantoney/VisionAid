import sounddevice as sd
import numpy as np
from transformers import pipeline

# Load the processor and model for Indian English
model_name = "Harveenchadha/vakyansh-wav2vec2-indian-english-enm-700"

# Using the pipeline for automatic speech recognition directly with model name
asr_pipeline = pipeline("automatic-speech-recognition", model=model_name)

# Set the expected sampling rate from the model's feature extractor
sampling_rate = asr_pipeline.feature_extractor.sampling_rate

# Function to capture real-time audio
def record_audio(duration=15):  # Set the desired duration
    print("Recording...")
    audio = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=1, dtype="float32")
    sd.wait()  # Wait for the recording to finish
    print("Recording finished.")
    return audio.squeeze()  # Return the audio array

# Real-time audio-to-text conversion
def real_time_speech_to_text(duration=15):  # Set the desired duration for the single input
    audio_array = record_audio(duration)  # Record audio for the entire duration

    # Transcribe the recorded audio
    transcription = asr_pipeline(audio_array)

    # Clean up the transcription
    cleaned_text = transcription['text'].replace("<s>", "").replace("</s>", "").replace("▁", " ").strip()

    print("Transcription:", cleaned_text)

# Start real-time speech-to-text with a total duration of 15 seconds
real_time_speech_to_text(duration=15)
