// Required libraries
const express = require('express');
const multer = require('multer');
const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const { Server } = require('socket.io');
const http = require('http');
const wav = require('wav');
const mic = require('mic');

const app = express();
const server = http.createServer(app);
const io = new Server(server);
const PORT = 3000;

// Route to serve the client HTML
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// Socket.io connection for real-time audio
io.on('connection', (socket) => {
  console.log('Client connected');

  // Start recording audio in real-time
  const micInstance = mic({
    rate: '16000',
    channels: '1',
    debug: false,
    fileType: 'wav',
  });

  const micInputStream = micInstance.getAudioStream();
  const wavWriter = new wav.FileWriter('realtime_audio.wav', {
    sampleRate: 16000,
    channels: 1,
  });

  micInputStream.pipe(wavWriter);

  micInstance.start();

  micInputStream.on('data', (data) => {
    console.log('Recording audio chunk');
    socket.emit('audio-data', data);
  });

  micInputStream.on('error', (err) => {
    console.error('Error in audio stream:', err);
  });

  socket.on('stop-recording', () => {
    console.log('Stopping recording');
    micInstance.stop();
    wavWriter.end();

    // Process the audio file with Python
    const pythonScript = path.join(__dirname, 'speech_to_text.py');
    const command = `python ${pythonScript} realtime_audio.wav`;

    exec(command, (error, stdout, stderr) => {
      if (error) {
        console.error(`Error: ${stderr}`);
        socket.emit('transcription-error', 'Error processing audio file.');
        return;
      }

      console.log(`Transcription: ${stdout}`);
      socket.emit('transcription-result', stdout.trim());

      // Clean up temporary audio file
      fs.unlink('realtime_audio.wav', (err) => {
        if (err) {
          console.error(`Error deleting file: ${err.message}`);
        }
      });
    });
  });

  socket.on('disconnect', () => {
    console.log('Client disconnected');
    micInstance.stop();
    wavWriter.end();
  });
});

// Start the server
server.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
