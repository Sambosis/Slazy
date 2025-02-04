C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
const express = require('express');
const path = require('path');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Middleware setup
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Set up EJS as the template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Sample sweater products data
const sweaters = [
    { id: 1, name: 'Classic Crewneck', price: 49.99, description: 'A timeless, comfortable crewneck sweater.', imageUrl: '/images/crewneck.jpg' },
    { id: 2, name: 'Cozy Cardigan', price: 59.99, description: 'A warm and stylish cardigan for layering.', imageUrl: '/images/cardigan.jpg' },
    { id: 3, name: 'Trendy Turtleneck', price: 54.99, description: 'A fashionable turtleneck sweater to keep you warm.', imageUrl: '/images/turtleneck.jpg' },
    { id: 4, name: 'Fair Isle Sweater', price: 69.99, description: 'A beautifully patterned Fair Isle sweater.', imageUrl: '/images/fairisle.jpg' }
];


// Routes
app.get('/', (req, res) => {
    res.render('index', { title: 'Sweater Store', sweaters: sweaters });
});

app.get('/sweaters', (req, res) => {
    res.render('sweaters', { title: 'Sweater Collection', sweaters: sweaters });
});

// Basic Error Handling - this should be placed after all routes
app.use((req, res, next) => {
    const error = new Error('Not found');
    error.status = 404;
    next(error);
});

app.use((error, req, res, next) => {
    res.status(error.status || 500);
    res.render('error', {
        title: 'Error',
        message: error.message,
        status: error.status
    });
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\layout.ejs
Language detected: ejs
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%- title %></title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="/">Sweater Store</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/sweaters">Sweaters</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container mt-4">
        <%- body %>
    </div>

    <footer class="footer mt-5 bg-light text-center py-3">
        <div class="container">
            <span>&copy; 2024 Sweater Store</span>
        </div>
    </footer>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

</body>
</html>
C:\mygit\BLazy\repo\nodetest\views\index.ejs
Language detected: ejs
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%- title %></title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <a class="navbar-brand" href="/">Sweater Store</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item active">
                    <a class="nav-link" href="/">Home <span class="sr-only">(current)</span></a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="/sweaters">Sweaters</a>
                </li>
            </ul>
        </div>
    </nav>

    <div class="container mt-4">
        <div class="jumbotron text-center">
            <h1 class="display-4">Welcome to the Sweater Store</h1>
            <p class="lead">Find your perfect sweater for any occasion.</p>
            <a class="btn btn-primary btn-lg" href="/sweaters" role="button">View All Sweaters</a>
        </div>

        <section class="featured-sweaters">
            <h2 class="text-center mb-4">Featured Sweaters</h2>
            <div class="row">
                <% featuredSweaters.forEach(sweater => { %>
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <img src="<%= sweater.imageUrl %>" class="card-img-top" alt="<%= sweater.name %>">
                            <div class="card-body">
                                <h5 class="card-title"><%= sweater.name %></h5>
                                <p class="card-text"><%= sweater.description %></p>
                                <p class="card-text"><strong>Price:</strong> $<%= sweater.price.toFixed(2) %></p>
                            </div>
                        </div>
                    </div>
                <% }); %>
            </div>
        </section>

        <section class="about mt-5">
            <h2 class="text-center mb-4">About Us</h2>
            <p class="lead text-center">We are dedicated to providing high-quality, comfortable, and stylish sweaters. Explore our collection and find the perfect addition to your wardrobe.</p>
        </section>
    </div>


    <footer class="footer mt-5 bg-light text-center py-3">
        <div class="container">
            <span>&copy; 2024 Sweater Store</span>
        </div>
    </footer>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>

</body>
</html>
C:\mygit\BLazy\repo\nodetest\data\sweaters.js
Language detected: javascript
// filepath: C:\mygit\BLazy\repo\nodetest\models\sweaters.js
module.exports = [
    {
        id: 1,
        name: 'Classic Crewneck',
        description: 'A timeless, comfortable crewneck sweater.',
        price: 49.99,
        imageUrl: '/images/crewneck.jpg',
        category: 'casual',
        sizes: ['S', 'M', 'L', 'XL'],
        colors: ['Gray', 'Navy', 'Black'],
         isFeatured: true,
    },
    {
        id: 2,
        name: 'Cozy Cardigan',
        description: 'A warm and stylish cardigan for layering.',
        price: 59.99,
        imageUrl: '/images/cardigan.jpg',
        category: 'casual',
        sizes: ['S', 'M', 'L', 'XL', 'XXL'],
        colors: ['Beige', 'Cream', 'Charcoal'],
        isFeatured: false,
    },
    {
        id: 3,
        name: 'Trendy Turtleneck',
        description: 'A fashionable turtleneck sweater to keep you warm.',
        price: 54.99,
        imageUrl: '/images/turtleneck.jpg',
        category: 'winter',
        sizes: ['XS', 'S', 'M', 'L'],
        colors: ['Burgundy', 'Forest Green', 'Off-White'],
         isFeatured: true,
    },
    {
        id: 4,
        name: 'Fair Isle Sweater',
        description: 'A beautifully patterned Fair Isle sweater.',
        price: 69.99,
        imageUrl: '/images/fairisle.jpg',
        category: 'winter',
        sizes: ['S', 'M', 'L', 'XL'],
        colors: ['Multi', 'Blue/White', 'Red/Black'],
         isFeatured: false,
    },
     {
        id: 5,
        name: 'Cashmere V-Neck',
        description: 'A luxurious cashmere V-neck sweater.',
        price: 129.99,
        imageUrl: '/images/cashmere.jpg',
        category: 'formal',
        sizes: ['S', 'M', 'L'],
        colors: ['Black', 'Gray' ,'Tan'],
         isFeatured: true,
    },
    {
        id: 6,
        name: 'Wool Zip-up',
          description: 'A warm wool zip-up sweater for outdoor activity.',
        price: 79.99,
        imageUrl: '/images/zipup.jpg',
         category: 'winter',
        sizes: ['M', 'L', 'XL', 'XXL'],
        colors: ['Navy', 'Olive', 'Brown'],
         isFeatured: false,
    },
     {
        id: 7,
        name: 'Cotton Pullover',
        description: 'A light and breathable cotton pullover.',
        price: 44.99,
        imageUrl: '/images/pullover.jpg',
        category: 'casual',
        sizes: ['XS', 'S', 'M', 'L', 'XL'],
         colors: ['White', 'Gray', 'LightBlue'],
          isFeatured: false,
    },
    {
        id: 8,
        name: 'Oversized Knit Sweater',
         description: 'A comfortable oversized knit sweater.',
         price: 64.99,
         imageUrl: '/images/oversized.jpg',
         category: 'casual',
         sizes: ['S/M', 'L/XL'],
         colors: ['Pink', 'Lavender', 'Mint'],
          isFeatured: true,
    },
    {
        id: 9,
        name: 'Cable Knit Sweater',
        description: 'A classic cable knit sweater.',
        price: 74.99,
        imageUrl: '/images/cableknit.jpg',
        category: 'winter',
       sizes: ['S', 'M', 'L'],
        colors: ['Cream', 'Navy', 'Maroon'],
         isFeatured: false,
    },
    {
        id: 10,
         name: 'Merino Wool Sweater',
        description: 'A soft and lightweight merino wool sweater.',
        price: 99.99,
        imageUrl: '/images/merino.jpg',
         category: 'formal',
        sizes: ['S', 'M', 'L', 'XL'],
         colors: ['Charcoal', 'Dark Teal', 'Light Gray'],
          isFeatured: false,
    }
];
C:\mygit\BLazy\repo\nodetest\package.json
Language detected: json
{
  "name": "sweater-store",
  "version": "1.0.0",
  "description": "A simple web application for browsing and showcasing a collection of sweaters.",
  "main": "app.js",
  "scripts": {
    "start": "node app.js",
    "dev": "nodemon app.js"
  },
  "dependencies": {
    "express": "^4.17.1",
    "ejs": "^3.1.6",
    "body-parser": "^1.19.0",
    "morgan": "^1.10.0"
  },
  "author": "Your Name",
  "license": "MIT"
}
