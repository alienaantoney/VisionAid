// Cameras.js
{/*
import React, { useState, useRef } from 'react';
import { View, Text, TouchableOpacity, Image, StyleSheet, Alert } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import axios from 'axios';

export default function Cameras2() {
  const { hasPermission, requestPermission } = useCameraPermission();
  const [capturedImage, setCapturedImage] = useState(null);
  const [caption, setCaption] = useState('');
  const cameraRef = useRef(null);

  const device = useCameraDevice('back');

  // Request camera permission
  if (!hasPermission) {
    requestPermission();
    return <Text>Requesting camera permission...</Text>;
  }
  if (!device) return <Text>No camera device found</Text>;

  const captureAndAnalyzeImage = async () => {
    if (!cameraRef.current) return;

    try {
      const photo = await cameraRef.current.takePhoto(); // Capture image
      setCapturedImage(`file://${photo.path}`);

      const formData = new FormData();
      formData.append('image', {
        uri: `file://${photo.path}`,
        name: 'captured.jpg',
        type: 'image/jpeg',
      });

      console.log('[DEBUG] Sending image for captioning...');
      const response = await axios.post('http://192.168.0.124:5000/generate_caption', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log('[DEBUG] Caption:', response.data.caption);
      setCaption(response.data.caption);

    } catch (error) {
      console.error('[ERROR] Failed to generate caption:', error);
      Alert.alert('Error', 'Failed to generate caption. Please try again.');
    }
  };

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={styles.camera}
        device={device}
        isActive={true}
        photo={true}
      />

      <TouchableOpacity style={styles.captureButton} onPress={captureAndAnalyzeImage}>
        <Text style={styles.buttonText}>Capture</Text>
      </TouchableOpacity>

      {capturedImage && <Image source={{ uri: capturedImage }} style={styles.previewImage} />}

      {caption !== '' && (
        <View style={styles.resultBox}>
          <Text style={styles.resultText}>📝 Caption: {caption}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  camera: { width: '100%', height: '70%' },
  captureButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    marginTop: 15,
  },
  buttonText: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  previewImage: {
    width: 150,
    height: 150,
    marginTop: 10,
    borderRadius: 10,
    borderWidth: 2,
    borderColor: '#007AFF',
  },
  resultBox: {
    position: 'absolute',
    bottom: 120,  // 👈 Adjust this value based on your tab bar height
    backgroundColor: 'rgba(0,0,0,0.7)',
    padding: 15,
    borderRadius: 10,
    width: '90%',
    alignSelf: 'center',
  },
  
  resultText: { color: 'white', fontSize: 16, fontWeight: 'bold' },
});
*/}
import React, { useState, useRef } from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Alert } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import axios from 'axios';

export default function Cameras() {
  const { hasPermission, requestPermission } = useCameraPermission();
  const [sceneInfo, setSceneInfo] = useState(null);
  const cameraRef = useRef(null);
  const device = useCameraDevice('back');

  if (!hasPermission) {
    requestPermission();
    return <Text>Requesting camera permission...</Text>;
  }
  if (!device) return <Text>No camera device found</Text>;

  const captureAndAnalyzeImage = async () => {
    if (!cameraRef.current) return;

    try {
      const photo = await cameraRef.current.takePhoto(); // Capture image

      // Prepare image data
      const formData = new FormData();
      formData.append('image', {
        uri: `file://${photo.path}`,
        name: 'scene.jpg',
        type: 'image/jpg',
      });

      console.log('[DEBUG] Sending image to backend...');
      const response = await axios.post('http://192.168.1.9:5000/generate_caption', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log('[DEBUG] Response:', response.data);
      setSceneInfo(response.data);

    } catch (error) {
      console.error('[ERROR] Failed to process image:', error);
      Alert.alert('Error', 'Failed to analyze scene. Please try again.');
    }
  };

  return (
    <View style={styles.container}>
      {/* Camera View */}
      <Camera
        ref={cameraRef}
        style={styles.camera}
        device={device}
        isActive={true}
        photo={true}
      />

      {/* Capture Button */}
      <TouchableOpacity style={styles.captureButton} onPress={captureAndAnalyzeImage}>
        <Text style={styles.buttonText}>Capture</Text>
      </TouchableOpacity>

      {/* Display Scene / Caption Information */}
      {sceneInfo && (
        <View style={styles.resultBox}>
          <Text style={styles.resultText}>📸 Description: {sceneInfo.caption}</Text>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  camera: { width: '100%', height: '70%' },
  captureButton: {
    backgroundColor: '#007AFF',
    padding: 15,
    borderRadius: 10,
    marginTop: 15,
  },
  buttonText: { color: 'white', fontSize: 18, fontWeight: 'bold' },
  resultBox: {
    backgroundColor: 'rgba(0,0,0,0.7)',
    padding: 15,
    borderRadius: 10,
    marginTop: 20, // 👈 Pushes output below the capture button
    width: '90%',
    alignSelf: 'center',
  },
  resultText: { color: 'white', fontSize: 16, fontWeight: 'bold', marginBottom: 5 },
});
