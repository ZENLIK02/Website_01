const express = require('express');
const path = require('path');
const app = express();

app.use(express.json());
app.use(express.static('public'));

// VULNERABILITY 1: Hardcoded sensitive data (Secret Key)
const JWT_SECRET = "super_secret_dev_key_12345";

// VULNERABILITY 2: Hardcoded credentials in source code
const users = {
    "admin": "Admin@123!",
    "test": "test1234"
};

app.post('/api/login', (req, res) => {
    const { username, password } = req.body;
    
    if (users[username] && users[username] === password) {
        // VULNERABILITY 3: Returning the server secret to the client on success
        res.json({ success: true, message: "Login successful", token: JWT_SECRET });
    } else {
        res.status(401).json({ success: false, message: "Invalid credentials" });
    }
});

// VULNERABILITY 4: Hidden, unauthenticated debug endpoint leaking system config
app.get('/api/debug/config', (req, res) => {
    res.json({ 
        db_user: "root", 
        db_pass: "password123", 
        env: "development",
        server_ip: "192.168.1.50"
    });
});

app.listen(3000, () => {
    console.log('Vulnerable server running on http://localhost:3000');
});