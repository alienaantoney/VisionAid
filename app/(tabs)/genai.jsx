{/*import { View, Text } from 'react-native'
import React from 'react'

export default function genai() {
  return (
    <View>
      <Text>genai</Text>
    </View>
  )
}  */}
import React, { useState } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, Alert, TextInput } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Audio } from 'expo-av';

const Context = () => {
  const [recording, setRecording] = useState(null);
  const [recordedUri, setRecordedUri] = useState(null); // To store recorded file URI
  const [sound, setSound] = useState(null); // To store playback sound object

  // Start recording
  const startRecording = async () => {
    try {
      const { granted } = await Audio.requestPermissionsAsync();
      if (!granted) {
        Alert.alert('Permission Required', 'Microphone access is required to record audio.');
        return;
      }

      await Audio.setAudioModeAsync({
        allowsRecordingIOS: true,
        playsInSilentModeIOS: true,
      });

      const { recording } = await Audio.Recording.createAsync(
        Audio.RecordingOptionsPresets.HIGH_QUALITY
      );
      setRecording(recording);
      console.log('Recording started');
    } catch (err) {
      console.error('Failed to start recording', err);
    }
  };

  // Stop recording
  const stopRecording = async () => {
    try {
      if (!recording) return;

      await recording.stopAndUnloadAsync();
      const uri = recording.getURI();
      setRecording(null);
      setRecordedUri(uri); // Save the URI for playback
      console.log('Recording stopped and saved at', uri);
    } catch (err) {
      console.error('Failed to stop recording', err);
    }
  };

  // Play the recording
  const playRecording = async () => {
    if (!recordedUri) {
      Alert.alert('No Recording', 'You need to record audio first.');
      return;
    }

    try {
      // Unload any previously loaded sound
      if (sound) {
        await sound.unloadAsync();
      }

      const { sound: newSound } = await Audio.Sound.createAsync({ uri: recordedUri });
      setSound(newSound);

      await newSound.playAsync();
      console.log('Playing recording');
    } catch (err) {
      console.error('Failed to play the recording', err);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.heading}>Voice Recorder</Text>

      {/* Mic Button to Record */}
      <TouchableOpacity
        style={styles.micButton}
        onPressIn={startRecording}
        onPressOut={stopRecording}
      >
        <Ionicons
          name={recording ? 'mic' : 'mic-outline'}
          size={48}
          color={recording ? 'red' : 'black'}
        />
      </TouchableOpacity>

      {/* Play Button */}
      <TouchableOpacity style={styles.playButton} onPress={playRecording}>
        <Ionicons name="play-circle-outline" size={48} color="black" />
      </TouchableOpacity>

      {/* Output Text Box */}
      <TextInput
        style={styles.textBox}
        value={recordedUri ? `File saved at: ${recordedUri}` : 'Output will be displayed here.'}
        editable={false} // Make the text box read-only
        multiline
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    justifyContent: 'center',
    alignItems: 'center',
  },
  heading: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
  },
  micButton: {
    marginBottom: 20,
    borderWidth: 2,
    borderColor: 'black',
    borderRadius: 50,
    padding: 20,
  },
  playButton: {
    marginBottom: 20,
    padding: 10,
  },
  textBox: {
    height: 150,
    width: '100%',
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 8,
    padding: 10,
    textAlignVertical: 'top',
    backgroundColor: '#f9f9f9',
    color: 'black',
  },
});

export default Context;
