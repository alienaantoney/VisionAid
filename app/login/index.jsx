import { View, Text, TouchableOpacity,StyleSheet } from 'react-native'
import React from 'react'
import {Image} from 'expo-image';
import Colors from '../../constant/Colors';
import { useRouter } from 'expo-router';

export default function LoginScreen() {
    const router=useRouter();
  return (
    <View>
      <View style={{
        display:'flex',
        alignitems:'center'
      }}>
        <Image source={require('./../../assets/images/welcome.jpg')}
        style={{width: 385, height: 400, borderRadius:23}} />
        

      </View>
      <View style={{
        padding:25,
        backgroundColor:Colors.PRIMARY,
        height:'100%'

      }}>
        <Text style={{
            fontSize:25,
            fontWeight:'bold',
            color:'white',
            textAlign:'center'
        }}>Empowering Independence, Enhancing Accessibility! </Text>
        <Text style={{
            color:'white',
            textAlign:'center',
            fontSize:16,
            marginTop:20
        }}>Assisting the visually impaired with voice-guided navigation, scene understanding, genAi assistance, and real-time obstacle detection.</Text>
        <TouchableOpacity style={styles?.button}
        onPress={() => router.push('login/signin')}>
            <Text style={{
                textAlign:'center',
                fontSize:15,
                color:Colors.PRIMARY
            }}>Get Started</Text>
        </TouchableOpacity>
      </View>
    </View>
  )
}
const styles =StyleSheet.create({
    button:{
        padding:15,
        backgroundColor:'white',
        borderRadius:99,
        marginTop:25
    }
})