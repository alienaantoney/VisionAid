{/*import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import axios from 'axios';

export default function CameraScreen() {
  const { hasPermission, requestPermission } = useCameraPermission();
  const [detectedObjects, setDetectedObjects] = useState([]);
  const cameraRef = useRef(null);

  useEffect(() => {
    async function getPermissions() {
      if (!hasPermission) await requestPermission();
    }
    getPermissions();
  }, [hasPermission]);

  const device = useCameraDevice('back');

  // 🔹 Function to capture image and send to backend
  const captureAndSendImage = async () => {
    if (!cameraRef.current) return;

    try {
      const photo = await cameraRef.current.takePhoto(); // Capture frame
      const formData = new FormData();
      formData.append('image', {
        uri: `file://${photo.path}`,
        name: 'frame.jpg',
        type: 'image/jpg',
      });

      console.log('[DEBUG] Sending frame to backend...');
      const response = await axios.post('http://192.168.1.9:5000/detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log('[DEBUG] Response from backend:', response.data);
      setDetectedObjects(response.data.objects);
    } catch (error) {
      console.error('[ERROR] Failed to send image:', error);
    }
  };

  if (!hasPermission) return <Text>Requesting camera permission...</Text>;
  if (!device) return <Text>No camera device found</Text>;

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true} // Enable photo mode
      />
      <TouchableOpacity style={styles.captureButton} onPress={captureAndSendImage}>
        <Text style={{ color: 'white' }}>Capture</Text>
      </TouchableOpacity>
      <View style={styles.overlay}>
        {detectedObjects.map((obj, index) => (
          <Text key={index} style={styles.objectText}>
            {obj.label} ({obj.confidence.toFixed(2)})
          </Text>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  captureButton: {
    position: 'absolute',
    bottom: 20,
    left: '40%',
    backgroundColor: 'blue',
    padding: 10,
    borderRadius: 10,
  },
  overlay: { position: 'absolute', top: 20, left: 20, backgroundColor: 'rgba(0,0,0,0.5)', padding: 10 },
  objectText: { color: 'white', fontSize: 16, marginBottom: 5 },
});
*/}
{/*import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, AccessibilityInfo } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import axios from 'axios';

export default function CameraScreen() {
  const { hasPermission, requestPermission } = useCameraPermission();
  const [detectedObjects, setDetectedObjects] = useState([]);
  const cameraRef = useRef(null);

  useEffect(() => {
    async function getPermissions() {
      if (!hasPermission) await requestPermission();
    }
    getPermissions();
  }, [hasPermission]);

  const device = useCameraDevice('back');

  // 🔹 Function to capture image and send to backend
  const captureAndSendImage = async () => {
    if (!cameraRef.current) return;

    try {
      const photo = await cameraRef.current.takePhoto(); // Capture frame
      const formData = new FormData();
      formData.append('image', {
        uri: `file://${photo.path}`,
        name: 'frame.jpg',
        type: 'image/jpg',
      });

      console.log('[DEBUG] Sending frame to backend...');
      const response = await axios.post('http://192.168.1.9:5000/detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log('[DEBUG] Response from backend:', response.data);
      setDetectedObjects(response.data.objects);

      // ✅ Read detected objects aloud
      if (response.data.objects.length > 0) {
        const objectNames = response.data.objects.map(obj => obj.label).join(', ');
        AccessibilityInfo.announceForAccessibility(`Detected objects: ${objectNames}`);
      } else {
        AccessibilityInfo.announceForAccessibility('No objects detected.');
      }

    } catch (error) {
      console.error('[ERROR] Failed to send image:', error);
      AccessibilityInfo.announceForAccessibility('Error processing image.');
    }
  };

  if (!hasPermission) return <Text>Requesting camera permission...</Text>;
  if (!device) return <Text>No camera device found</Text>;

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true} // Enable photo mode
      />
      <TouchableOpacity style={styles.captureButton} onPress={captureAndSendImage}>
        <Text style={styles.buttonText}>Capture</Text>
      </TouchableOpacity>
      <View style={styles.overlay}>
        {detectedObjects.map((obj, index) => (
          <Text key={index} style={styles.objectText}>
            {obj.label} ({obj.confidence.toFixed(2)})
          </Text>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  captureButton: {
    position: 'absolute',
    bottom: 20,
    left: '40%',
    backgroundColor: 'blue',
    padding: 10,
    borderRadius: 10,
  },
  buttonText: { color: 'white', fontSize: 16 },
  overlay: { position: 'absolute', top: 20, left: 20, backgroundColor: 'rgba(0,0,0,0.5)', padding: 10 },
  objectText: { color: 'white', fontSize: 16, marginBottom: 5 },
});
*/}
{/*
import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet, AccessibilityInfo } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import axios from 'axios';

export default function CameraScreen() {
  const { hasPermission, requestPermission } = useCameraPermission();
  const [detectedObjects, setDetectedObjects] = useState([]);
  const cameraRef = useRef(null);

  useEffect(() => {
    async function getPermissions() {
      if (!hasPermission) await requestPermission();
    }
    getPermissions();

    // ✅ Capture image every 5 seconds
    const interval = setInterval(() => {
      captureAndSendImage();
    }, 5000); // 5 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, [hasPermission]);

  const device = useCameraDevice('back');

  // ✅ Capture & send image to backend
  const captureAndSendImage = async () => {
    if (!cameraRef.current) return;

    try {
      const photo = await cameraRef.current.takePhoto(); // Capture frame
      const formData = new FormData();
      formData.append('image', {
        uri: `file://${photo.path}`,
        name: 'frame.jpg',
        type: 'image/jpg',
      });

      console.log('[DEBUG] Sending frame to backend...');
      const response = await axios.post('http://192.168.1.9:5000/detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log('[DEBUG] Response from Flask:', response.data);
      setDetectedObjects(response.data.objects);

      // ✅ Announce detected objects for screen reader
      if (response.data.objects.length > 0) {
        const objectNames = response.data.objects.map(obj => obj.label).join(', ');
        AccessibilityInfo.announceForAccessibility(`Detected objects: ${objectNames}`);
      }

    } catch (error) {
      console.error('[ERROR] Failed to send image:', error);
    }
  };

  if (!hasPermission) return <Text>Requesting camera permission...</Text>;
  if (!device) return <Text>No camera device found</Text>;

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true} // ✅ Required for capturing images
      />
      <View style={styles.overlay}>
        {detectedObjects.map((obj, index) => (
          <Text key={index} style={styles.objectText}>
            {obj.label} ({obj.confidence.toFixed(2)})
          </Text>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  overlay: { 
    position: 'absolute', 
    top: 20, 
    left: 20, 
    backgroundColor: 'rgba(0,0,0,0.5)', 
    padding: 10,
    borderRadius: 10,
  },
  objectText: { 
    color: 'white', 
    fontSize: 16, 
    marginBottom: 5 
  },
});
*/}
import React, { useState, useEffect, useRef } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { Camera, useCameraDevice, useCameraPermission } from 'react-native-vision-camera';
import axios from 'axios';
import * as Speech from 'expo-speech'; // Import expo-speech

export default function CameraScreen() {
  const { hasPermission, requestPermission } = useCameraPermission();
  const [detectedObjects, setDetectedObjects] = useState([]);
  const cameraRef = useRef(null);

  useEffect(() => {
    async function getPermissions() {
      if (!hasPermission) await requestPermission();
    }
    getPermissions();

    // Capture image every 5 seconds
    const interval = setInterval(() => {
      captureAndSendImage();
    }, 5000); // 5 seconds

    return () => clearInterval(interval); // Cleanup on unmount
  }, [hasPermission]);

  const device = useCameraDevice('back');

  // Capture & send image to backend
  const captureAndSendImage = async () => {
    if (!cameraRef.current) return;

    try {
      const photo = await cameraRef.current.takePhoto(); // Capture frame
      const formData = new FormData();
      formData.append('image', {
        uri: `file://${photo.path}`,
        name: 'frame.jpg',
        type: 'image/jpg',
      });

      console.log('[DEBUG] Sending frame to backend...');
      const response = await axios.post('http://192.168.1.9:5000/detect', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      console.log('[DEBUG] Response from Flask:', response.data);
      setDetectedObjects(response.data.objects);

      // ✅ Announce detected objects using expo-speech
      if (response.data.objects.length > 0) {
        const objectNames = response.data.objects.map(obj => obj.label).join(', ');
        Speech.speak(`Detected objects: ${objectNames}`); // Use expo-speech to speak
      }

    } catch (error) {
      console.error('[ERROR] Failed to send image:', error);
    }
  };

  if (!hasPermission) return <Text>Requesting camera permission...</Text>;
  if (!device) return <Text>No camera device found</Text>;

  return (
    <View style={styles.container}>
      <Camera
        ref={cameraRef}
        style={StyleSheet.absoluteFill}
        device={device}
        isActive={true}
        photo={true} // Required for capturing images
      />
      <View style={styles.overlay}>
        {detectedObjects.map((obj, index) => (
          <Text key={index} style={styles.objectText}>
            {obj.label} ({obj.confidence.toFixed(2)})
          </Text>
        ))}
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  overlay: { 
    position: 'absolute', 
    top: 20, 
    left: 20, 
    backgroundColor: 'rgba(0,0,0,0.5)', 
    padding: 10,
    borderRadius: 10,
  },
  objectText: { 
    color: 'white', 
    fontSize: 16, 
    marginBottom: 5 
  },
});