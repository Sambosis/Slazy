C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
const express = require('express');
const bodyParser = require('body-parser');
const morgan = require('morgan');
const path = require('path');

const app = express();
const port = 3000;

// Set up EJS as the template engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Use body-parser for parsing request bodies
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


// Use Morgan for logging
app.use(morgan('dev'));

// Sample sweater products
const products = [
    {
        id: 1,
        name: 'Classic Wool Sweater',
        description: 'A warm and cozy sweater made from 100% wool.',
        price: 79.99,
        image: '/images/sweater1.jpg'
    },
    {
        id: 2,
        name: 'Cotton V-Neck Sweater',
        description: 'A comfortable and stylish cotton sweater.',
        price: 59.99,
        image: '/images/sweater2.jpg'
    },
    {
        id: 3,
        name: 'Cashmere Turtleneck',
        description: 'A luxurious cashmere turtleneck sweater.',
        price: 199.99,
        image: '/images/sweater3.jpg'
    }
];

// Routes
app.get('/', (req, res) => {
    res.render('index',{
        title: 'Home - Sweater Store'
    });
});

app.get('/products', (req, res) => {
    res.render('products', {
        title: 'Products - Sweater Store',
        products: products
    });
});


// Basic error handling
app.use((err, req, res, next) => {
    console.error(err.stack);
    res.status(500).send('Something broke!');
});


app.use((req, res, next) => {
    res.status(404).send("Sorry, can't find that!");
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\layout.ejs
Language detected: ejs
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%= title %></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            font-family: sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        nav {
            background-color: #343a40;
        }
         .navbar-brand{
            color: #ffffff
        }
        nav a {
            color: #fff;
            text-decoration: none;
            padding: 10px 15px;
            display: inline-block;
        }

        main {
            flex: 1;
            padding: 20px;
             background-color: #f8f9fa;
        }
       

        footer {
            background-color: #343a40;
            color: #fff;
            text-align: center;
            padding: 10px;
            margin-top: 20px;
        }
             .navbar-nav {
                margin-left: auto;
            }
         .navbar-nav .nav-link {
                color: #ffffff;
           }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg">
        <div class="container">
          <a class="navbar-brand" href="/">Sweater Store</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item">
                <a class="nav-link" href="/">Home</a>
              </li>
              <li class="nav-item">
                <a class="nav-link" href="/products">Products</a>
              </li>
            </ul>
          </div>
        </div>
    </nav>
    <main>
        <%- body %>
    </main>
    <footer>
        &copy; <%= new Date().getFullYear() %> Sweater Store
    </footer>

     <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
