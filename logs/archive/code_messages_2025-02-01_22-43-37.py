C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
const express = require('express');
const path = require('path');
const morgan = require('morgan');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Configure middleware
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));

// Set EJS as view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Sample sweater data
const sweaters = [
  {
    id: 1,
    name: 'Cozy Cable Knit',
    description: 'A classic cable knit sweater for ultimate warmth.',
    price: 59.99,
    imageUrl: '/images/sweater1.jpg',
  },
  {
    id: 2,
    name: 'Striped Merino Wool',
    description: 'Soft merino wool sweater with stylish stripes.',
    price: 79.99,
    imageUrl: '/images/sweater2.jpg',
  },
    {
    id: 3,
    name: 'Chunky Turtleneck',
    description: 'Warm and comfortable chunky turtleneck sweater',
    price: 64.99,
       imageUrl: '/images/sweater3.jpg',
  },
    {
        id: 4,
        name: 'Fair Isle Sweater',
        description: 'A festive fair isle pattern for the holidays',
        price: 89.99,
        imageUrl: '/images/sweater4.jpg',
    }
];

// Routes
app.get('/', (req, res) => {
  res.render('index', { sweaters });
});


app.get('/sweater/:id', (req, res) => {
    const sweaterId = parseInt(req.params.id);
    const sweater = sweaters.find((s) => s.id === sweaterId);

    if (sweater) {
        res.render('sweater', { sweater });
    }
  else {
      res.status(404).send('Sweater Not Found');
    }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\index.ejs
Language detected: html
<!-- filepath: C:\mygit\BLazy\repo\nodetest\views\index.ejs -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sweater Shop</title>
    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="/styles/style.css">
</head>
<body>
    <%- include('layout') %>
    <div class="container mt-4">
        <h1 class="mb-4">Welcome to Our Sweater Collection!</h1>
        <div class="row">
            <% sweaters.forEach(sweater => { %>
                <div class="col-md-4 mb-4">
                    <div class="card">
                        <img src="<%= sweater.imageUrl %>" class="card-img-top" alt="<%= sweater.name %>">
                        <div class="card-body">
                            <h5 class="card-title"><%= sweater.name %></h5>
                            <p class="card-text">Price: $<%= sweater.price %></p>
                            <p class="card-text"><%= sweater.description %></p>
                            <a href="/sweater/<%= sweater.id %>" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                </div>
            <% }); %>
        </div>
    </div>
    <!-- Bootstrap JS and dependencies -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\data\sweaters.js
Language detected: javascript
// filepath: C:\mygit\BLazy\repo\nodetest\sweatersData.js
const sweaters = [
    {
        id: 1,
        name: 'Classic Crewneck Sweater',
        price: 69.99,
        shortDescription: 'A timeless crewneck for everyday wear.',
         longDescription: 'This classic crewneck sweater features a comfortable fit and is perfect for layering or wearing on its own. Made from high-quality materials, it offers both style and durability.',
        imageUrl: 'https://placekitten.com/200/300',
        availableSizes: ['S', 'M', 'L', 'XL'],
        materialComposition: '100% Cotton',
        careInstructions: 'Machine wash cold, tumble dry low',
        availableColors: ['Navy', 'Gray', 'Charcoal', 'White']
      },
    {
        id: 2,
        name: 'Wool Blend Turtleneck',

        price: 89.99,
        shortDescription: 'Warm and stylish turtleneck for colder days.',
        longDescription: 'Stay cozy in our wool blend turtleneck sweater. The high neckline and soft material provide extra warmth, making it an ideal choice for chilly weather. Its modern design makes it suitable for both casual and dressier occasions.',
        imageUrl: 'https://placekitten.com/201/301',
        availableSizes: ['XS', 'S', 'M', 'L'],
        materialComposition: '50% Wool, 50% Acrylic',
        careInstructions: 'Hand wash cold, lay flat to dry',
        availableColors: ['Black', 'Beige', 'Burgundy']
    },
    {
        id: 3,
        name: 'Striped Cotton Sweater',
        price: 54.99,
        shortDescription: 'Casual striped sweater for a relaxed look.',
         longDescription: 'This striped cotton sweater is perfect for adding a touch of casual style to your wardrobe. Its soft and breathable fabric ensures all-day comfort, while its timeless design makes it a versatile piece.',
        imageUrl: 'https://placekitten.com/202/302',
        availableSizes: ['S', 'M', 'L', 'XL','XXL'],
        materialComposition: '100% Cotton',
        careInstructions: 'Machine wash cold, tumble dry low',
        availableColors: ['Blue/White', 'Red/White', 'Green/White']
    },
      {
        id: 4,
        name: 'Chunky Cable Knit Sweater',
        price: 99.99,
        shortDescription: 'Cozy cable knit sweater for ultimate warmth.',
         longDescription: 'Our chunky cable knit sweater is crafted from a blend of soft, warm yarn and features intricate cable knit detailing. This sweater provides ultimate warmth and comfort, making it perfect for cold weather days.',
        imageUrl: 'https://placekitten.com/203/303',
        availableSizes: ['S', 'M', 'L'],
        materialComposition: '70% Acrylic, 30% Wool',
        careInstructions: 'Hand wash cold, lay flat to dry',
        availableColors: ['Cream', 'Gray', 'Navy']
    },
  {
        id: 5,
        name: 'Oversized V-Neck Sweater',
        price: 74.99,
        shortDescription: 'Relaxed oversized v-neck for easy styling.',
       longDescription: "Embrace comfort and style with our oversized V-neck sweater. Its relaxed fit and dropped shoulders make it perfect for layering or wearing on its own. The versatile design allows for easy styling and will add an element of effortless chic to your look.",
        imageUrl: 'https://placekitten.com/204/304',
          availableSizes: ['XS','S', 'M', 'L', 'XL'],
        materialComposition: '60% Cotton 40% Polyester',
        careInstructions: 'Machine wash cold, tumble dry low',
          availableColors: ['Light Pink','Light Blue','Lavender']
    },
    {
        id: 6,
        name: 'Fair Isle Pattern Sweater',
        price: 109.99,
        shortDescription: 'Festive Fair Isle sweater for the holidays.',
        longDescription: 'Our stylish Fair Isle sweater is adorned with a classic festive pattern and made with a soft blend. Sure to be a favorite, it will provide you with both comfort and an element of sophisticated fun.',
        imageUrl: 'https://placekitten.com/205/305',
        availableSizes: ['S', 'M', 'L', 'XL'],
        materialComposition: '55% Wool, 45% Other',
           careInstructions: 'Dry clean only',
           availableColors: ['Multi-color']
    }
];

module.exports = sweaters;
