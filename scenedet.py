'''
import torch
from torch.autograd import Variable as V
import torchvision.models as models
from torchvision import transforms as trn
from torch.nn import functional as F
import os
import numpy as np
import cv2
from PIL import Image
import urllib.request

features_blobs = []

# Download helper
def download_file(url, filename):
    if not os.path.exists(filename):
        print(f'Downloading {filename}...')
        urllib.request.urlretrieve(url, filename)

# Fix BatchNorm for PyTorch 1.x
def recursion_change_bn(module):
    if isinstance(module, torch.nn.BatchNorm2d):
        module.track_running_stats = 1
    else:
        for i, (name, module1) in enumerate(module._modules.items()):
            module1 = recursion_change_bn(module1)
    return module

def load_labels():
    # Categories
    file_name_category = 'categories_places365.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt', file_name_category)
    classes = []
    with open(file_name_category) as f:
        for line in f:
            classes.append(line.strip().split(' ')[0][3:])
    classes = tuple(classes)

    # IO Labels (Fixed loading)
    file_name_IO = 'IO_places365.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/IO_places365.txt', file_name_IO)
    labels_IO = []
    with open(file_name_IO) as f:
        for line in f:
            parts = line.strip().split()
            labels_IO.append(int(parts[1]) - 1)  # 0 = indoor, 1 = outdoor
    labels_IO = np.array(labels_IO)

    # Scene Attributes
    file_name_attribute = 'labels_sunattribute.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/labels_sunattribute.txt', file_name_attribute)
    with open(file_name_attribute) as f:
        labels_attribute = [line.strip() for line in f]

    file_name_W = 'W_sceneattribute_wideresnet18.npy'
    download_file('http://places2.csail.mit.edu/models_places365/W_sceneattribute_wideresnet18.npy', file_name_W)
    W_attribute = np.load(file_name_W)

    return classes, labels_IO, labels_attribute, W_attribute

def hook_feature(module, input, output):
    features_blobs.append(np.squeeze(output.data.cpu().numpy()))

def returnTF():
    return trn.Compose([
        trn.Resize((224, 224)),
        trn.ToTensor(),
        trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def load_model():
    model_file = 'wideresnet18_places365.pth.tar'
    download_file('http://places2.csail.mit.edu/models_places365/wideresnet18_places365.pth.tar', model_file)
    
    # wideresnet.py is needed
    wideresnet_file = 'wideresnet.py'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/wideresnet.py', wideresnet_file)

    import importlib.util
    spec = importlib.util.spec_from_file_location("wideresnet", wideresnet_file)
    wideresnet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wideresnet)

    model = wideresnet.resnet18(num_classes=365)
    checkpoint = torch.load(model_file, map_location=lambda storage, loc: storage)
    state_dict = {k.replace('module.', ''): v for k, v in checkpoint['state_dict'].items()}
    model.load_state_dict(state_dict)

    model = recursion_change_bn(model)
    model.avgpool = torch.nn.AvgPool2d(kernel_size=14, stride=1, padding=0)
    model.eval()

    # Hook the feature extractor
    model._modules.get('layer4').register_forward_hook(hook_feature)
    model._modules.get('avgpool').register_forward_hook(hook_feature)
    return model

if __name__ == '__main__':
    # Load labels and model
    classes, labels_IO, labels_attribute, W_attribute = load_labels()
    model = load_model()
    tf = returnTF()

    # Get softmax weights
    params = list(model.parameters())
    weight_softmax = params[-2].data.numpy()
    weight_softmax[weight_softmax < 0] = 0

    # Load test image (Change the path to your test image)
    img_path = 'bedroom.jpg'  # Ensure this image is in your project folder
    if not os.path.exists(img_path):
        print(f"Image {img_path} not found!")
        exit()

    img = Image.open(img_path).convert('RGB')
    input_img = V(tf(img).unsqueeze(0))

    # Forward pass
    logit = model.forward(input_img)
    h_x = F.softmax(logit, 1).data.squeeze()
    probs, idx = h_x.sort(0, True)
    probs, idx = probs.numpy(), idx.numpy()

    # Top prediction
    top_scene_idx = idx[0]
    top_scene_prob = probs[0]
    top_scene_name = classes[top_scene_idx]

    # Determine indoor or outdoor
    io_image = labels_IO[top_scene_idx]
    environment = "indoor" if io_image == 0 else "outdoor"
    print(f'--TYPE OF ENVIRONMENT: {environment}')

    # Scene Category
    print(f'--SCENE CATEGORY: {top_scene_name} ---> {top_scene_prob:.3f}')

    # Scene Attributes
    responses_attribute = W_attribute.dot(features_blobs[1])
    idx_a = np.argsort(responses_attribute)
    scene_attributes = ', '.join([labels_attribute[idx_a[i]] for i in range(-1, -10, -1)])
    print(f'--SCENE ATTRIBUTES: {scene_attributes}')
'''
'''
import torch
from torch.autograd import Variable as V
import torchvision.models as models
from torchvision import transforms as trn
from torch.nn import functional as F
import os
import numpy as np
import urllib.request
from PIL import Image
from flask import Flask, request, jsonify

features_blobs = []

# Download helper
def download_file(url, filename):
    if not os.path.exists(filename):
        print(f'Downloading {filename}...')
        urllib.request.urlretrieve(url, filename)

# Fix BatchNorm for PyTorch 1.x
def recursion_change_bn(module):
    if isinstance(module, torch.nn.BatchNorm2d):
        module.track_running_stats = 1
    else:
        for i, (name, module1) in enumerate(module._modules.items()):
            module1 = recursion_change_bn(module1)
    return module

def load_labels():
    # Categories
    file_name_category = 'categories_places365.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt', file_name_category)
    classes = [line.strip().split(' ')[0][3:] for line in open(file_name_category)]
    classes = tuple(classes)

    # IO Labels (fixed loading)
    file_name_IO = 'IO_places365.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/IO_places365.txt', file_name_IO)
    labels_IO = []
    with open(file_name_IO) as f:
        for line in f:
            parts = line.strip().split()
            labels_IO.append(int(parts[1]) - 1)  # 0 = indoor, 1 = outdoor
    labels_IO = np.array(labels_IO)

    # Scene Attributes
    file_name_attribute = 'labels_sunattribute.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/labels_sunattribute.txt', file_name_attribute)
    labels_attribute = [line.strip() for line in open(file_name_attribute)]

    file_name_W = 'W_sceneattribute_wideresnet18.npy'
    download_file('http://places2.csail.mit.edu/models_places365/W_sceneattribute_wideresnet18.npy', file_name_W)
    W_attribute = np.load(file_name_W)

    return classes, labels_IO, labels_attribute, W_attribute

def hook_feature(module, input, output):
    features_blobs.append(np.squeeze(output.data.cpu().numpy()))

def returnTF():
    return trn.Compose([
        trn.Resize((224, 224)),
        trn.ToTensor(),
        trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

def load_model():
    model_file = 'wideresnet18_places365.pth.tar'
    download_file('http://places2.csail.mit.edu/models_places365/wideresnet18_places365.pth.tar', model_file)

    wideresnet_file = 'wideresnet.py'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/wideresnet.py', wideresnet_file)

    import importlib.util
    spec = importlib.util.spec_from_file_location("wideresnet", wideresnet_file)
    wideresnet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wideresnet)

    model = wideresnet.resnet18(num_classes=365)
    checkpoint = torch.load(model_file, map_location=lambda storage, loc: storage)
    state_dict = {k.replace('module.', ''): v for k, v in checkpoint['state_dict'].items()}
    model.load_state_dict(state_dict)

    model = recursion_change_bn(model)
    model.avgpool = torch.nn.AvgPool2d(kernel_size=14, stride=1, padding=0)
    model.eval()

    # Hook feature extractors
    model._modules.get('layer4').register_forward_hook(hook_feature)
    model._modules.get('avgpool').register_forward_hook(hook_feature)
    return model

# ------------------- Scene Detection Flask API -------------------
app = Flask(__name__)

classes, labels_IO, labels_attribute, W_attribute = load_labels()
model = load_model()
tf = returnTF()

params = list(model.parameters())
weight_softmax = params[-2].data.numpy()
weight_softmax[weight_softmax < 0] = 0

@app.route('/analyze', methods=['POST'])
def analyze_scene():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    img_file = request.files['image']
    img = Image.open(img_file.stream).convert('RGB')

    global features_blobs
    features_blobs = []

    input_img = V(tf(img).unsqueeze(0))
    logit = model.forward(input_img)
    h_x = F.softmax(logit, 1).data.squeeze()
    probs, idx = h_x.sort(0, True)
    probs, idx = probs.numpy(), idx.numpy()

    top_scene_idx = idx[0]
    top_scene_name = classes[top_scene_idx]
    environment = "indoor" if labels_IO[top_scene_idx] == 0 else "outdoor"

    # Scene attributes
    responses_attribute = W_attribute.dot(features_blobs[1])
    idx_a = np.argsort(responses_attribute)
    scene_attributes = [labels_attribute[idx_a[i]] for i in range(-1, -10, -1)]

    response = {
        "Environment": environment,
        "Scene Category": top_scene_name,
        "Scene Attributes": scene_attributes
    }
    return jsonify(response)

# ------------------- CLI Testing -------------------
if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        # CLI image test
        test_img_path = 'bedroom.jpg'
        if not os.path.exists(test_img_path):
            print(f"Test image '{test_img_path}' not found.")
            exit()

        img = Image.open(test_img_path).convert('RGB')
        input_img = V(tf(img).unsqueeze(0))
        logit = model.forward(input_img)
        h_x = F.softmax(logit, 1).data.squeeze()
        probs, idx = h_x.sort(0, True)
        probs, idx = probs.numpy(), idx.numpy()

        top_scene_idx = idx[0]
        top_scene_prob = probs[0]
        top_scene_name = classes[top_scene_idx]
        environment = "indoor" if labels_IO[top_scene_idx] == 0 else "outdoor"

        print(f'--TYPE OF ENVIRONMENT: {environment}')
        print(f'--SCENE CATEGORY: {top_scene_name} ---> {top_scene_prob:.3f}')

        responses_attribute = W_attribute.dot(features_blobs[1])
        idx_a = np.argsort(responses_attribute)
        scene_attributes = ', '.join([labels_attribute[idx_a[i]] for i in range(-1, -10, -1)])
        print(f'--SCENE ATTRIBUTES: {scene_attributes}')
'''
import torch
from torch.autograd import Variable as V
import torchvision.models as models
from torchvision import transforms as trn
from torch.nn import functional as F
import os
import numpy as np
import urllib.request
from PIL import Image
from flask import Flask, request, jsonify

features_blobs = []

# Helper to download required files
def download_file(url, filename):
    if not os.path.exists(filename):
        print(f'Downloading {filename}...')
        urllib.request.urlretrieve(url, filename)

# Fix batch norm for compatibility
def recursion_change_bn(module):
    if isinstance(module, torch.nn.BatchNorm2d):
        module.track_running_stats = 1
    else:
        for name, module1 in module._modules.items():
            module1 = recursion_change_bn(module1)
    return module

# Load labels and mappings
def load_labels():
    # Categories
    file_category = 'categories_places365.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/categories_places365.txt', file_category)
    classes = [line.strip().split(' ')[0][3:] for line in open(file_category)]
    classes = tuple(classes)

    # Indoor/Outdoor labels
    file_IO = 'IO_places365.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/IO_places365.txt', file_IO)
    labels_IO = []
    with open(file_IO) as f:
        for line in f:
            parts = line.strip().split()
            labels_IO.append(int(parts[1]) - 1)  # 0 = indoor, 1 = outdoor
    labels_IO = np.array(labels_IO)

    # Scene attributes
    file_attribute = 'labels_sunattribute.txt'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/labels_sunattribute.txt', file_attribute)
    labels_attribute = [line.strip() for line in open(file_attribute)]

    file_W = 'W_sceneattribute_wideresnet18.npy'
    download_file('http://places2.csail.mit.edu/models_places365/W_sceneattribute_wideresnet18.npy', file_W)
    W_attribute = np.load(file_W)

    return classes, labels_IO, labels_attribute, W_attribute

def hook_feature(module, input, output):
    features_blobs.append(np.squeeze(output.data.cpu().numpy()))

def return_transform():
    return trn.Compose([
        trn.Resize((224, 224)),
        trn.ToTensor(),
        trn.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])

# Load the model
def load_model():
    model_file = 'wideresnet18_places365.pth.tar'
    download_file('http://places2.csail.mit.edu/models_places365/wideresnet18_places365.pth.tar', model_file)

    wideresnet_file = 'wideresnet.py'
    download_file('https://raw.githubusercontent.com/csailvision/places365/master/wideresnet.py', wideresnet_file)

    import importlib.util
    spec = importlib.util.spec_from_file_location("wideresnet", wideresnet_file)
    wideresnet = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wideresnet)

    model = wideresnet.resnet18(num_classes=365)
    checkpoint = torch.load(model_file, map_location=torch.device('cpu'),weights_only=True)
    state_dict = {k.replace('module.', ''): v for k, v in checkpoint['state_dict'].items()}
    model.load_state_dict(state_dict)

    model = recursion_change_bn(model)
    model.avgpool = torch.nn.AvgPool2d(kernel_size=14, stride=1, padding=0)
    model.eval()

    model._modules.get('layer4').register_forward_hook(hook_feature)
    model._modules.get('avgpool').register_forward_hook(hook_feature)
    return model

# Initialize Flask App
app = Flask(__name__)

# Load labels, model, and transformations once
classes, labels_IO, labels_attribute, W_attribute = load_labels()
model = load_model()
tf = return_transform()
params = list(model.parameters())
weight_softmax = params[-2].data.numpy()
weight_softmax[weight_softmax < 0] = 0

# API Route for Scene Analysis
@app.route('/analyze', methods=['POST'])
def analyze_scene():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    img_file = request.files['image']
    img = Image.open(img_file.stream).convert('RGB')

    global features_blobs
    features_blobs = []

    input_img = V(tf(img).unsqueeze(0))
    logit = model.forward(input_img)
    h_x = F.softmax(logit, 1).data.squeeze()
    probs, idx = h_x.sort(0, True)
    probs, idx = probs.numpy(), idx.numpy()

    top_scene_idx = idx[0]
    top_scene_name = classes[top_scene_idx]
    environment = "indoor" if labels_IO[top_scene_idx] == 0 else "outdoor"

    # Scene attributes
    responses_attribute = W_attribute.dot(features_blobs[1])
    idx_a = np.argsort(responses_attribute)
    scene_attributes = [labels_attribute[idx_a[i]] for i in range(-1, -10, -1)]

    response = {
        "Environment": environment,
        "Scene Category": top_scene_name,
        "Scene Attributes": scene_attributes
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
