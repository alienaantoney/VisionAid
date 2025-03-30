'''
from flask import Flask, request, jsonify
import torch
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
import os

app = Flask(__name__)

# Load BLIP model and processor once when the app starts
print("[INFO] Loading BLIP model...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
print("[INFO] Model loaded successfully!")

def generate_caption(image_path):
    try:
        raw_image = Image.open(image_path).convert('RGB')
        inputs = processor(raw_image, return_tensors="pt")

        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)

        return caption
    except Exception as e:
        print(f"[ERROR] Caption generation failed: {e}")
        return "Could not generate caption."

@app.route('/generate_caption', methods=['POST'])
def caption_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image = request.files['image']
    image_path = f"temp_{image.filename}"
    image.save(image_path)

    # Generate caption
    caption_text = generate_caption(image_path)

    # Clean up the saved image
    os.remove(image_path)

    return jsonify({'caption': caption_text})

if __name__ == "__main__":
    # Run the app on all network interfaces (for mobile device access)
    app.run(host='0.0.0.0', port=5000)
'''
from flask import Flask, request, jsonify
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch
import os

app = Flask(__name__)

# Load BLIP model and processor once
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

@app.route('/generate_caption', methods=['POST'])
def caption_route():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image_path = 'temp_captured.jpg'
    image_file.save(image_path)

    try:
        # Open and process the image
        raw_image = Image.open(image_path).convert('RGB')
        inputs = processor(raw_image, return_tensors="pt")

        # Generate caption
        output = model.generate(**inputs)
        caption = processor.decode(output[0], skip_special_tokens=True)

        return jsonify({'caption': caption})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        # Safely remove the image file
        if os.path.exists(image_path):
            os.remove(image_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
