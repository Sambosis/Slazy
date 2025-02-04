C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
const express = require('express');
const bodyParser = require('body-parser');
const morgan = require('morgan');
const path = require('path');

const app = express();
const port = 3000;

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views')); // Set views directory

// Middleware setup
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));  // Serve static files (CSS, images)

// Mock database of sweaters
const sweaters = [
    { id: 1, name: 'Cozy Cable Knit', price: 59.99, image: '/images/sweater1.jpg', description: 'A classic cable knit sweater perfect for chilly days.' },
    { id: 2, name: 'Striped Merino Wool', price: 79.99, image: '/images/sweater2.jpg',  description: 'A stylish striped sweater made from soft merino wool.'},
    { id: 3, name: 'Oversized Fleece', price: 49.99, image: '/images/sweater3.jpg',  description: 'A comfortable and warm oversized fleece sweater.' },
    { id: 4, name: 'Colorblock Cotton', price: 69.99, image: '/images/sweater4.jpg',  description: 'A modern colorblock design for a stylish look.'}
];

// Routes
app.get('/', (req, res) => {
  const featuredSweaters = sweaters.slice(0,2); // Example of featured selection
  res.render('index', { featuredSweaters });
});

app.get('/products', (req, res) => {
    res.render('products', { sweaters });
});

app.get('/about', (req, res) => {
    res.render('about');
});


// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\index.ejs
Language detected: html
<!-- filepath: C:\mygit\BLazy\repo\nodetest\views\index.ejs -->
<%- include('layout', {pageTitle: 'Home'}) %>

<div class="container">
    <!-- Hero Section -->
    <div class="jumbotron text-center bg-primary text-white">
        <h1>Welcome to Our Sweater Store</h1>
        <p>Find the perfect sweater for any occasion.</p>
    </div>

    <!-- Featured Products Section -->
    <div class="py-4">
        <h2>Featured Products</h2>
        <div class="row">
            <% featuredSweaters.forEach(sweater => { %>
                <div class="col-md-3 mb-4">
                    <div class="card h-100">
                        <img src="<%= sweater.image %>" class="card-img-top" alt="<%= sweater.name %>">
                        <div class="card-body">
                            <h5 class="card-title"><%= sweater.name %></h5>
                            <p class="card-text">$<%= sweater.price %></p>
                            <p class="card-text"><%= sweater.description %></p>
                            <a href="/products" class="btn btn-primary">Shop Now</a>
                        </div>
                    </div>
                </div>
            <% }); %>
        </div>
    </div>
     <!-- Promotional Section -->
    <div class="bg-light py-5">
        <div class="container text-center">
            <h2>Special Offers</h2>
            <p>Check out our latest discounts and limited-time offers!</p>
            <a href="/products" class="btn btn-success">View All Offers</a>
        </div>
    </div>
</div>
C:\mygit\BLazy\repo\nodetest\views\products.ejs
Language detected: html
<!-- filepath: C:\mygit\BLazy\repo\nodetest\views\products.ejs -->
<%- include('layout', {pageTitle: 'Products'}) %>

<div class="container">
    <div class="row">
        <!-- Filter Sidebar -->
        <div class="col-md-3">
            <div class="filter-sidebar">
                <h3>Filter</h3>
                <div class="mb-3">
                    <h5>Categories</h5>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="cardigans">
                        <label class="form-check-label" for="cardigans">Cardigans</label>
                    </div>
                     <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="pullovers">
                        <label class="form-check-label" for="pullovers">Pullovers</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="wool">
                       <label class="form-check-label" for="wool">Wool</label>
                   </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="cotton">
                        <label class="form-check-label" for="cotton">Cotton</label>
                    </div>
                </div>
                <div class="mb-3">
                    <h5>Price Range</h5>
                    <input type="range" class="form-range" min="0" max="100" step="10" id="priceRange">
                    <p>Range: $<span id="priceRangeValue">50</span></p>
                </div>
                <div class="mb-3">
                    <h5>Size</h5>
                     <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="sizeS">
                        <label class="form-check-label" for="sizeS">S</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="sizeM">
                        <label class="form-check-label" for="sizeM">M</label>
                    </div>
                     <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="sizeL">
                        <label class="form-check-label" for="sizeL">L</label>
                    </div>
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="" id="sizeXL">
                        <label class="form-check-label" for="sizeXL">XL</label>
                    </div>
                </div>
            </div>
        </div>

        <!-- Product Grid -->
        <div class="col-md-9">
            <div class="d-flex justify-content-between align-items-center mb-3">
                <h2>All Products</h2>
                <div class="sort-options">
                  <label for="sortBy">Sort by:</label>
                    <select id="sortBy" class="form-select form-select-sm">
                        <option value="price-low">Price: Low to High</option>
                        <option value="price-high">Price: High to Low</option>
                       <option value="newest">Newest</option>
                    </select>
                </div>
            </div>
            <div class="row">
                <% sweaters.forEach(sweater => { %>
                    <div class="col-md-4 mb-4">
                        <div class="card h-100">
                            <img src="<%= sweater.image %>" class="card-img-top" alt="<%= sweater.name %>">
                            <div class="card-body">
                                <h5 class="card-title"><%= sweater.name %></h5>
                                <p class="card-text">$<%= sweater.price %></p>
                                  <p class="card-text">
                                    Available Sizes: <span class="badge bg-secondary">S</span>
                                                      <span class="badge bg-secondary">M</span>
                                                     <span class="badge bg-secondary">L</span>
                                                    <span class="badge bg-secondary">XL</span>
                                </p>
                                 <div class="d-flex justify-content-between">
                                      <button class="btn btn-secondary btn-sm">Quick View</button>
                                      <button class="btn btn-primary btn-sm">Add to Cart</button>
                                  </div>
                            </div>
                        </div>
                    </div>
                <% }); %>
            </div>
              <!-- Pagination -->
            <nav aria-label="Page navigation">
                <ul class="pagination justify-content-center">
                  <li class="page-item disabled">
                    <span class="page-link">Previous</span>
                  </li>
                  <li class="page-item active"><a class="page-link" href="#">1</a></li>
                  <li class="page-item"><a class="page-link" href="#">2</a></li>
                  <li class="page-item"><a class="page-link" href="#">3</a></li>
                  <li class="page-item">
                    <a class="page-link" href="#">Next</a>
                  </li>
                </ul>
              </nav>
        </div>
    </div>
</div>
<script>
    document.getElementById('priceRange').addEventListener('input', function() {
        document.getElementById('priceRangeValue').textContent = this.value;
    });
</script>
