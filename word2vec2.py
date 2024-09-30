import sounddevice as sd
import torch
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
import numpy as np

# Load the processor and model
model_name = "facebook/wav2vec2-base-960h"  # Wav2Vec2 model for English
processor = Wav2Vec2Processor.from_pretrained(model_name)
model = Wav2Vec2ForCTC.from_pretrained(model_name).to("cpu")  # Use CPU

# Set the expected sampling rate
sampling_rate = processor.feature_extractor.sampling_rate

# Function to capture real-time audio
def record_audio(duration=5):
    print("Recording...")
    audio = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=1, dtype="float32")
    sd.wait()  # Wait for the recording to finish
    print("Recording finished.")
    return audio.squeeze()  # Return the audio array

# Function to process and transcribe the real-time audio
import numpy as np

def transcribe_audio(audio_array):
    # Assuming `model` and `processor` are already defined
    input_values = processor(audio_array, return_tensors="pt", padding=True).input_values
    with torch.no_grad():
        logits = model(input_values).logits
    # Get the predicted token ids (argmax on the logits)
    predicted_ids = torch.argmax(logits, dim=-1)
    # Decode the predicted ids
    transcription = processor.batch_decode(predicted_ids.cpu().numpy())
    return transcription



# Real-time audio-to-text conversion
def real_time_speech_to_text():
    # Step 1: Record audio for a specified duration (e.g., 5 seconds)
    audio_array = record_audio()  # Replace with your audio recording function
    transcription = transcribe_audio(audio_array)

    # Check if the transcription is not empty and access the first element
    if transcription and transcription[0].lower() == "exit":
        print("Exiting the transcription...")
        return

    print("Transcription:", transcription)

# Start real-time speech-to-text
real_time_speech_to_text()
