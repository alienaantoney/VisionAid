{/*import { View, Text } from 'react-native'
import React from 'react'

export default function context() {
  return (
    <View>
      <Text>context</Text>
    </View>
  )
}
  */}

import 'react-native-reanimated'; // MUST be first import!
import React from "react";
import { SafeAreaView } from "react-native";
import Cameras2 from "../camera2"; 


export default function context() {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <Cameras2/> 
    </SafeAreaView>
  );
}