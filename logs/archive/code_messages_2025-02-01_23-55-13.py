C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const port = 3000;

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Set up static file serving
app.use(express.static(path.join(__dirname, 'public')));

// Set up middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


// Mock Database (Replace with actual MongoDB connection for real app)
const sweaters = [
  { id: 1, name: 'Classic Wool Sweater', price: 79.99, image: '/images/sweater1.jpg',description: "A warm classic wool sweater"},
  { id: 2, name: 'Cotton Knit Sweater', price: 59.99, image: '/images/sweater2.jpg',description: "A comfortable cotton knit sweater" },
  { id: 3, name: 'Cashmere Blend Sweater', price: 129.99, image: '/images/sweater3.jpg', description: "A luxurious cashmere blend sweater"},
  { id: 4, name: 'Fleece Pullover', price: 49.99, image: '/images/sweater4.jpg', description:"A soft lightweight fleece pullover."}
];


let cart = [];

// Routes
app.get('/', (req, res) => {
  res.render('index', { sweaters });
});

app.get('/sweater/:id', (req, res) => {
  const sweaterId = parseInt(req.params.id);
  const sweater = sweaters.find(sweater => sweater.id === sweaterId);
  if (sweater) {
    res.render('sweater', { sweater });
  } else {
      res.status(404).send('Sweater not found');
  }
});

app.post('/add-to-cart', (req, res) => {
    const sweaterId = parseInt(req.body.sweaterId);
    const sweater = sweaters.find(sweater => sweater.id === sweaterId);
  if (sweater) {
    cart.push(sweater);
      res.redirect('/cart');
  } else
    res.status(404).send('Sweater not found.')
});

app.get('/cart', (req, res) => {
  res.render('cart', { cart });
});


// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\layout.ejs
Language detected: python
# filepath: C:\mygit\BLazy\repo\nodetest\app.js
const express = require('express');
const mongoose = require('mongoose');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const port = 3000;

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Set up static file serving
app.use(express.static(path.join(__dirname, 'public')));

// Set up middleware
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


// Mock Database (Replace with actual MongoDB connection for real app)
const sweaters = [
  { id: 1, name: 'Classic Wool Sweater', price: 79.99, image: '/images/sweater1.jpg',description: "A warm classic wool sweater"},
  { id: 2, name: 'Cotton Knit Sweater', price: 59.99, image: '/images/sweater2.jpg',description: "A comfortable cotton knit sweater" },
  { id: 3, name: 'Cashmere Blend Sweater', price: 129.99, image: '/images/sweater3.jpg', description: "A luxurious cashmere blend sweater"},
  { id: 4, name: 'Fleece Pullover', price: 49.99, image: '/images/sweater4.jpg', description:"A soft lightweight fleece pullover."}
];


let cart = [];

// Routes
app.get('/', (req, res) => {
  res.render('index', { sweaters });
});

app.get('/sweater/:id', (req, res) => {
  const sweaterId = parseInt(req.params.id);
  const sweater = sweaters.find(sweater => sweater.id === sweaterId);
  if (sweater) {
    res.render('sweater', { sweater });
  } else {
      res.status(404).send('Sweater not found');
  }
});

app.post('/add-to-cart', (req, res) => {
    const sweaterId = parseInt(req.body.sweaterId);
    const sweater = sweaters.find(sweater => sweater.id === sweaterId);
  if (sweater) {
    cart.push(sweater);
      res.redirect('/cart');
  } else
    res.status(404).send('Sweater not found.')
});

app.get('/cart', (req, res) => {
  res.render('cart', { cart });
});


// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\index.ejs
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sweater Store</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">

</head>
<body>
    <%- include('partials/header') %>

    <div class="container mt-5">
        <div class="jumbotron text-center">
            <h1 class="display-4">Welcome to Our Sweater Store</h1>
            <p class="lead">Find the perfect sweater for any occasion.</p>
            <hr class="my-4">
            <div class="featured-sweater">
                <% if (sweaters && sweaters.length > 0) { %>
                    <% const featured = sweaters[0]; %>
                <div class="featured-sweater-container">
                    <img src="<%= featured.image %>" alt="<%= featured.name %>" class="img-fluid featured-image">
                    <div class="featured-content">
                        <h3><%= featured.name %></h3>
                        <p> <%= featured.description %></p>
                         <p class="font-weight-bold">$<%= featured.price.toFixed(2) %></p>
                        <a href="/sweater/<%= featured.id %>" class="btn btn-primary">View Details</a>
                    </div>
                </div>
                <% } else { %>
                    <p>No sweaters available.</p>
                <% } %>
            </div>

        </div>

        <div class="row">
            <div class="col-md-3">
                
                <div class="card">
                  <div class="card-header">
                    Filter Options
                  </div>
                    <ul class="list-group list-group-flush">
                        <li class="list-group-item">
                            <strong>Categories:</strong>
                        </li>
                       <li class="list-group-item">
                            <div class="form-check">
                                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck1">
                                  <label class="form-check-label" for="defaultCheck1">
                                    Wool
                                 </label>
                            </div>
                            <div class="form-check">
                                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck2">
                                  <label class="form-check-label" for="defaultCheck2">
                                    Cotton
                                 </label>
                            </div>
                            <div class="form-check">
                                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck3">
                                  <label class="form-check-label" for="defaultCheck3">
                                    Cashmere
                                 </label>
                            </div>
                            <div class="form-check">
                                  <input class="form-check-input" type="checkbox" value="" id="defaultCheck4">
                                  <label class="form-check-label" for="defaultCheck4">
                                     Fleece
                                 </label>
                            </div>
                      </li>
                      <li class="list-group-item">
                        <strong>Price:</strong>
                      </li>
                      <li class="list-group-item">
                           <label for="minPrice">Min:</label>
                            <input type="number" class="form-control" id="minPrice" placeholder="Min Price">
                      </li>
                       <li class="list-group-item">
                           <label for="maxPrice">Max:</label>
                           <input type="number" class="form-control" id="maxPrice" placeholder="Max Price">
                       </li>
                    </ul>
                 <div class="card-body">
                     <button class="btn btn-primary">Apply filters</button>
                   </div>
                </div>
            </div>
            <div class="col-md-9">
                <div class="row">
                    <% if (sweaters && sweaters.length > 0) { %>
                        <% sweaters.forEach(sweater => { %>
                            <div class="col-md-4 mb-4">
                                <div class="card h-100">
                                    <img src="<%= sweater.image %>" alt="<%= sweater.name %>" class="card-img-top img-fluid product-image">
                                    <div class="card-body">
                                        <h5 class="card-title"><%= sweater.name %></h5>
                                        <p class="card-text font-weight-bold">$<%= sweater.price.toFixed(2) %></p>
                                        
                                         <div class="d-flex justify-content-between align-items-center">
                                            <a href="/sweater/<%= sweater.id %>" class="btn btn-sm btn-outline-secondary">Quick View</a>
                                            <form action="/add-to-cart" method="post">
                                                <input type="hidden" name="sweaterId" value="<%= sweater.id %>">
                                                <button type="submit" class="btn btn-sm btn-success">Add to Cart</button>
                                            </form>
                                         </div>
                                    </div>
                                </div>
                            </div>
                        <% }); %>
                    <% } else { %>
                        <div class="col">
                            <p>No sweaters available.</p>
                        </div>
                    <% } %>
                </div>
            </div>
        </div>
    </div>
      <%- include('partials/footer') %>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\views\product.ejs
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%= sweater.name %> - Sweater Store</title>
    <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
     <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    <style>
        .product-image-large {
            max-width: 100%;
            height: auto;
        }
       .product-thumbnail {
            max-width: 80px;
            height: auto;
            cursor: pointer;
            margin: 5px;
            border: 1px solid #ddd;
            padding: 2px;
        }

        .product-thumbnail.active {
           border-color: #007bff;
           }

    </style>
</head>
<body>
    <%- include('partials/header') %>
  <div class="container mt-5">
        <div class="row">
            <div class="col-md-6">
                <img id="main-image" src="<%= sweater.image %>" alt="<%= sweater.name %>" class="product-image-large">
                <div class="mt-2">
                    <img src="<%= sweater.image %>" alt="<%= sweater.name %>" class="product-thumbnail active" data-image="<%= sweater.image %>">
                    <img src="/images/sweater1.jpg" alt="<%= sweater.name %> Secondary" class="product-thumbnail" data-image="/images/sweater1.jpg">
                     <img src="/images/sweater2.jpg" alt="<%= sweater.name %> Secondary" class="product-thumbnail" data-image="/images/sweater2.jpg">

                </div>
            </div>
            <div class="col-md-6">
                <h2><%= sweater.name %></h2>
                <p class="font-weight-bold">$<%= sweater.price.toFixed(2) %></p>
                <p><%= sweater.description %></p>

                <div class="mt-3">
                  <label for="size">Size:</label>
                    <select class="form-control" id="size">
                      <option>S</option>
                      <option>M</option>
                      <option>L</option>
                     <option>XL</option>
                    </select>
                </div>
                <div class="mt-3">
                   <label for="color">Color:</label>
                    <select class="form-control" id="color">
                      <option>Gray</option>
                       <option>Navy</option>
                      <option>Black</option>
                       <option>Red</option>
                       <option>Green</option>
                    </select>
                </div>
                  <div class="mt-3">
                      <label for="quantity">Quantity:</label>
                      <input type="number" class="form-control" id="quantity" value="1" min="1">
                  </div>
                  <div class="mt-3">
                    <form action="/add-to-cart" method="post">
                        <input type="hidden" name="sweaterId" value="<%= sweater.id %>">
                        <button type="submit" class="btn btn-success">Add to Cart</button>
                    </form>
                </div>
                <div class="mt-3">
                  <button type="button" class="btn btn-link" data-toggle="modal" data-target="#sizeGuideModal">
                    Size Guide
                  </button>
                </div>


            </div>
        </div>

     <div class="mt-5">
            <ul class="nav nav-tabs" id="productTabs" role="tablist">
                <li class="nav-item">
                    <a class="nav-link active" id="description-tab" data-toggle="tab" href="#description" role="tab" aria-controls="description" aria-selected="true">Description</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" id="materials-tab" data-toggle="tab" href="#materials" role="tab" aria-controls="materials" aria-selected="false">Materials</a>
                </li>
                 <li class="nav-item">
                   <a class="nav-link" id="care-tab" data-toggle="tab" href="#care" role="tab" aria-controls="care" aria-selected="false">Care Instructions</a>
                </li>
            </ul>
              <div class="tab-content" id="productTabsContent">
                <div class="tab-pane fade show active" id="description" role="tabpanel" aria-labelledby="description-tab">
                     <p><%= sweater.description %> </p>
                </div>
                <div class="tab-pane fade" id="materials" role="tabpanel" aria-labelledby="materials-tab">
                    <p> 100% Wool</p>
                </div>
                 <div class="tab-pane fade" id="care" role="tabpanel" aria-labelledby="care-tab">
                    <p>Machine wash cold, tumble dry low</p>
                </div>
             </div>
        </div>



         <% if (relatedProducts && relatedProducts.length > 0) { %>
         <h3 class="mt-5">Related Products</h3>
        <div class ="row">
            <% relatedProducts.forEach(related => { %>
                 <div class="col-md-4 mb-4">
                     <div class="card h-100">
                         <img src="<%= related.image %>" alt="<%= related.name %>" class="card-img-top img-fluid product-image">
                         <div class="card-body">
                           <h5 class="card-title"><%= related.name %></h5>
                           <p class="card-text font-weight-bold">$<%= related.price.toFixed(2) %></p>
                            <div class="d-flex justify-content-between align-items-center">
                              <a href="/sweater/<%= related.id %>" class="btn btn-sm btn-outline-secondary">Quick View</a>
                                  <form action="/add-to-cart" method="post">
                                        <input type="hidden" name="sweaterId" value="<%= related.id %>">
                                        <button type="submit" class="btn btn-sm btn-success">Add to Cart</button>
                                  </form>
                            </div>
                         </div>
                     </div>
                 </div>
            <% }); %>
        </div>
          <% } %>
        <div class="mt-5">
            <h3>Customer Reviews</h3>
            <p>No Reviews yet.</p>
             </div>
        </div>
<div class="modal fade" id="sizeGuideModal" tabindex="-1" role="dialog" aria-labelledby="sizeGuideModalLabel" aria-hidden="true">
  <div class="modal-dialog" role="document">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title" id="sizeGuideModalLabel">Size Guide</h5>
        <button type="button" class="close" data-dismiss="modal" aria-label="Close">
          <span aria-hidden="true">&times;</span>
        </button>
      </div>
      <div class="modal-body">
          <table class="table">
              <thead>
                  <tr>
                    <th>Size</th>
                    <th>Chest(in)</th>
                    <th>Length(in)</th>
                   </tr>
                </thead>
              <tbody>
                   <tr>
                      <td>S</td>
                      <td>34-36</td>
                      <td>27</td>
                   </tr>
                    <tr>
                      <td>M</td>
                      <td>38-40</td>
                       <td>28</td>
                   </tr>
                     <tr>
                       <td>L</td>
                       <td>42-44</td>
                       <td>29</td>
                    </tr>
                     <tr>
                        <td>XL</td>
                        <td>46-48</td>
                        <td>30</td>
                     </tr>
                </tbody>
            </table>
      </div>
    </div>
  </div>
</div>
    <%- include('partials/footer') %>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function () {
            const thumbnails = document.querySelectorAll('.product-thumbnail');
            const mainImage = document.getElementById('main-image');

            thumbnails.forEach(thumb => {
                thumb.addEventListener('click', function () {
                     thumbnails.forEach(t => t.classList.remove('active'));
                    this.classList.add('active');
                    mainImage.src = this.getAttribute('data-image');
                });
            });
        });
    </script>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\models\Sweater.js
Language detected: python
const mongoose = require('mongoose');

const sweaterSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true,
  },
  price: {
    type: Number,
    required: true,
    min: 0,
  },
  description: {
    type: String,
    trim: true,
  },
  images: {
      type: [String],
       default: [],
    },
    sizes: {
        type: [String],
        default: ["S", "M", "L", "XL"]
    },
   colors: [{
        name: {
          type:String,
          required:true
        },
         hexCode:{
           type:String,
           required:true
         }
      }],
  category: {
    type: String,
    trim: true,
  },
    materials: {
        type: [String],
        default: []
    },
  careInstructions: {
      type: String,
       trim: true,
  },
  inStock: {
    type: Boolean,
    default: true,
  },
  featured: {
    type: Boolean,
     default: false,
  },
  createdAt: {
    type: Date,
    default: Date.now,
  },
});

const Sweater = mongoose.model('Sweater', sweaterSchema);

module.exports = Sweater;
