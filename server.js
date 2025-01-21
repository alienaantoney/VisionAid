require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const { registerUser, loginUser } = require('./user'); // Import functions from user.js


const app = express();
app.use(bodyParser.json());

// User Routes
app.post('/register', registerUser);
app.post('/login', async (req, res) => {
    await loginUser(req, res);
});


// Start Server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
