import { View, Text } from 'react-native';
import React from 'react';
import { Tabs } from 'expo-router';
import FontAwesome from '@expo/vector-icons/FontAwesome';
import Ionicons from '@expo/vector-icons/Ionicons';
import Foundation from '@expo/vector-icons/Foundation';
import * as Speech from 'expo-speech'; // Import the speech library
import { TouchableOpacity } from 'react-native';


export default function TabLayout() {
  const tabNames = {
    index: 'Map and Navigation',
    cloning: 'Voice Cloning',
    genai: 'Generative AI Notes',
    context: 'Context and Scene Description',
  };

  const handleTabPress = (tabKey) => {
    if (Speech.isSpeakingAsync()) {
      Speech.stop(); // Stop any ongoing speech
    }
    Speech.speak(tabNames[tabKey]); // Speak the selected tab's description
  };
  return (
    <Tabs>
        <Tabs.Screen name='index'
         options={{
            tabBarIcon: ({ color, size }) => (
              <FontAwesome name="map-marker" size={size} color="black" />
            ),
            tabBarButton: (props) => (
              <TouchableOpacity
                {...props}
                onPress={() => {
                  handleTabPress('index'); // Trigger speech
                  props.onPress?.(); // Perform default tab action
                }}
              />
            ),
          }}/>
        <Tabs.Screen name='cloning'
         options={{
            tabBarIcon: ({ color, size }) => (
              <Ionicons name="mic-circle-outline" size={size} color="black" />
            ),
            tabBarButton: (props) => (
              <TouchableOpacity
                {...props}
                onPress={() => {
                  handleTabPress('cloning'); // Trigger speech
                  props.onPress?.(); // Perform default tab action
                }}
              />
            ),
          }}/>
        <Tabs.Screen name='genai'
        options={{
            tabBarIcon: ({ color, size }) => (
              <Foundation name="clipboard-notes" size={size} color="black" />
            ),
            tabBarButton: (props) => (
              <TouchableOpacity
                {...props}
                onPress={() => {
                  handleTabPress('genai'); // Trigger speech
                  props.onPress?.(); // Perform default tab action
                }}
              />
            ),
          }}/>
        <Tabs.Screen name='context'
          options={{
            tabBarIcon: ({ color, size }) => (
              <FontAwesome name="eye" size={size} color="black" />
              
            ),
            tabBarButton: (props) => (
              <TouchableOpacity
                {...props}
                onPress={() => {
                  handleTabPress('context'); // Trigger speech
                  props.onPress?.(); // Perform default tab action
                }}
              />
            ),
          }}/>

    </Tabs>
  )
}