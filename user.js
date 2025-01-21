require('dotenv').config();
const mongoose = require('mongoose');
const bcrypt = require('bcrypt');
const jwt = require('jsonwebtoken');

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI, {
    useNewUrlParser: true,
    useUnifiedTopology: true,
    dbName: 'visionaid', // Database name
})
.then(() => console.log('MongoDB connected'))
.catch(err => console.error('MongoDB connection error:', err));

// User Schema
const userSchema = new mongoose.Schema({
    username: { type: String, required: true, unique: true },
    email: { type: String, required: true, unique: true },
    password: { type: String, required: true },
});

// Model for User
const User = mongoose.model('User', userSchema, 'user');

// Register Route
async function registerUser(req, res) {
    const { username, email, password } = req.body;

    try {
        // Check if the user already exists
        const existingUser = await User.findOne({ email });
        if (existingUser) return res.status(400).json({ error: 'User already exists' });

        // Hash the password
        const hashedPassword = await bcrypt.hash(password, 10);

        // Create a new user
        const user = new User({ username, email, password: hashedPassword });
        await user.save();

        res.status(201).json({ message: 'User registered successfully' });
    } catch (err) {
        res.status(500).json({ error: 'Error registering user', details: err });
    }
}

// Login Route
async function loginUser(req, res) {
    const { email, password } = req.body;

    try {
        // Find the user
        const user = await User.findOne({ email });
        if (!user) return res.status(400).json({ error: 'Invalid credentials' });

        // Compare passwords
        const isPasswordValid = await bcrypt.compare(password, user.password);
        if (!isPasswordValid) return res.status(400).json({ error: 'Invalid credentials' });

        // Generate a JWT token
        const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: '1h' });

        res.json({ message: 'Login successful', token });
    } catch (err) {
        res.status(500).json({ error: 'Error logging in', details: err });
    }
}

module.exports = {
    registerUser,
    loginUser
};

