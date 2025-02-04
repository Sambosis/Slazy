C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
// Import necessary modules
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

// Initialize the express app
const app = express();

// Set up middleware
// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));
// Parse incoming request bodies
app.use(bodyParser.urlencoded({ extended: false }));
// Set the view engine to EJS
app.set('view engine', 'ejs');

// Mock database of sweaters
const sweaters = [
    { id: 1, name: 'Cozy Crewneck', color: 'Gray', price: 45, image: '/images/gray_sweater.jpg', description: 'Comfortable and classic crewneck sweater perfect for any occasion.' },
    { id: 2, name: 'Rainbow Stripe', color: 'Multicolor', price: 55, image: '/images/rainbow_sweater.jpg', description: 'Bright and fun rainbow striped sweater to add a pop of color.' },
    { id: 3, name: 'Cable Knit Cardigan', color: 'Cream', price: 65, image: '/images/cream_sweater.jpg', description: 'Warm and stylish cable knit cardigan, great for layering.' },
    { id: 4, name: 'Bold Blue Hoodie', color: 'Blue', price: 50, image: '/images/blue_hoodie.jpg', description: 'Casual and comfortable blue hoodie, perfect for everyday wear.' },
    { id: 5, name: 'Forest Green Turtleneck', color: 'Green', price: 60, image: '/images/green_turtleneck.jpg', description: 'Warm and elegant forest green turtleneck for stylish winter looks.'}
];


// Define routes
// Homepage - displays all sweaters
app.get('/', (req, res) => {
    res.render('index', { sweaters: sweaters });
});

// Individual sweater page
app.get('/sweater/:id', (req, res) => {
    const sweaterId = parseInt(req.params.id);
   const sweater = sweaters.find(sweat => sweat.id === sweaterId);
    if (sweater) {
        res.render('sweater', { sweater: sweater });
    } else {
        res.status(404).send('Sweater not found');
    }
});


// About page
app.get('/about', (req, res) => {
    res.render('about');
});

// Start the server
const port = 3000;
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
