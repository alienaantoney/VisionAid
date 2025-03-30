{/*import { View, Text } from 'react-native'
import React from 'react'
import { Redirect } from 'expo-router';
export default function HomeScreen() {
  return (
    <View>
      <Text>HomeScreen</Text>
    </View>
  )
}
*/}

import 'react-native-reanimated'; // MUST be first import!
import React from "react";
import { SafeAreaView } from "react-native";
import CameraScreen from "../camerascreen"; 


export default function HomeScreen() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <CameraScreen /> 
    </SafeAreaView>
  );
}

