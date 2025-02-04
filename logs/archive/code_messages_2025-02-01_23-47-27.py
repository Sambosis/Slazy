C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');

const app = express();
const port = 3000;

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));


// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Body parser middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

// Mock data for sweater products
const products = [
    { id: 1, name: 'Classic Wool Sweater', price: 79.99, description: 'A timeless wool sweater for all occasions.' },
    { id: 2, name: 'Cozy Knit Cardigan', price: 69.99, description: 'A comfortable knitted cardigan perfect for chilly evenings.' },
    { id: 3, name: 'Stylish Turtleneck Sweater', price: 89.99, description: 'A fashionable turtleneck sweater to keep you warm and stylish.' },
    { id: 4, name: 'Lightweight Cotton Sweater', price: 59.99, description: 'A soft and light cotton sweater, ideal for layering.' },
    { id: 5, name: 'Hooded Fleece Sweater', price: 64.99, description: 'A comfortable fleece sweater for casual wear.'}
];

// Routes
app.get('/', (req, res) => {
    res.render('index', {title: 'Home'});
});

app.get('/products', (req, res) => {
    res.render('products', { products: products, title: 'Products' });
});

app.get('/product/:id', (req, res) => {
    const productId = parseInt(req.params.id);
    const product = products.find(p => p.id === productId);
    if (product) {
      res.render('product', { product: product, title: `Product: ${product.name}` });
    } else {
      res.status(404).send('Product not found');
    }
  });



// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\header.ejs
Language detected: html
<!DOCTYPE html>
 <html lang="en">
 <head>
     <meta charset="UTF-8">
     <meta name="viewport" content="width=device-width, initial-scale=1.0">
     <title><%= title || 'Cozy Sweaters' %></title>
     <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
     <link rel="stylesheet" href="/css/style.css">
 </head>
 <body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Cozy Sweaters</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
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
    </nav>


     <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
     <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
     <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
C:\mygit\BLazy\repo\nodetest\views\footer.ejs
Language detected: html
<!-- filepath: C:\mygit\BLazy\repo\nodetest\views\footer.ejs -->
 <footer class="mt-5 bg-light text-center">
    <div class="container py-3">
        <p>&copy; <%= new Date().getFullYear() %> Cozy Sweaters. All rights reserved.</p>
        <p>Contact us: <a href="mailto:info@cozysweaters.com">info@cozysweaters.com</a></p>
        <div class="social-links">
            <a href="#" target="_blank" rel="noopener noreferrer">Facebook</a> |
            <a href="#" target="_blank" rel="noopener noreferrer">Twitter</a> |
            <a href="#" target="_blank" rel="noopener noreferrer">Instagram</a>
        </div>
    </div>
</footer>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\views\index.ejs
Language detected: html
<!-- filepath: C:\mygit\BLazy\repo\nodetest\views\index.ejs -->
<%- include('header') %>

    <div class="container mt-4">
        <section class="jumbotron text-center">
            <h1 class="display-4">Welcome to Cozy Sweaters</h1>
            <p class="lead">Find the perfect sweater to keep you warm and stylish.</p>
            <hr class="my-4">
            <p>We offer a wide range of high-quality sweaters for every style and occasion.</p>
        </section>

        <section class="featured-products mt-5">
            <h2 class="text-center mb-4">Featured Sweaters</h2>
            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Classic Wool Sweater</h5>
                            <p class="card-text">A timeless wool sweater for all occasions.</p>
                            <a href="/product/1" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                 </div>
                  <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Cozy Knit Cardigan</h5>
                            <p class="card-text">A comfortable knitted cardigan perfect for chilly evenings.</p>
                            <a href="/product/2" class="btn btn-primary">View Details</a>
                        </div>
                     </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">Stylish Turtleneck Sweater</h5>
                            <p class="card-text">A fashionable turtleneck sweater to keep you warm and stylish.</p>
                            <a href="/product/3" class="btn btn-primary">View Details</a>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="about-us mt-5">
            <h2 class="text-center mb-4">About Us</h2>
            <p class="lead text-center">At Cozy Sweaters, we are passionate about providing you with the best quality sweaters. We believe that everyone deserves to feel comfortable and stylish, which is why we carefully curate our collection to offer a wide variety of options for all tastes and preferences.</p>
        </section>

        <div class="text-center mt-5 mb-5">
            <a href="/products" class="btn btn-lg btn-success">View All Products</a>
        </div>
    </div>

<%- include('footer') %>
C:\mygit\BLazy\repo\nodetest\views\products.ejs
Language detected: ejs
<!-- filepath: C:\mygit\BLazy\repo\nodetest\views\products.ejs -->
<%- include('header') %>

<div class="container mt-4">
    <h1 class="text-center mb-4">Our Sweaters Collection</h1>

     <section class="mb-4 text-center">
        <div class="d-inline-block mr-3">
            <label for="filter" class="mr-2">Filter By:</label>
            <select id="filter" class="form-control form-control-sm d-inline-block" style="width: auto;">
                <option value="all">All</option>
                <option value="wool">Wool</option>
               <option value="cotton">Cotton</option>

            </select>
        </div>
        <div class="d-inline-block">
            <label for="sort" class="mr-2">Sort By:</label>
            <select id="sort" class="form-control form-control-sm d-inline-block" style="width: auto;">
                <option value="name">Name</option>
                <option value="price">Price</option>
            </select>
        </div>

    </section>
    <div class="row">
        <% if (products && products.length > 0) { %>
              <% products.forEach(product => { %>
            <div class="col-md-4 mb-4">
                <div class="card h-100">
                      <img src="/images/sweater_placeholder.png" class="card-img-top" alt="<%= product.name %>" style="height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h5 class="card-title"><%= product.name %></h5>
                        <p class="card-text">Price: $<%= product.price %></p>
                        <p class="card-text"><%= product.description %></p>
                        <a href="/product/<%= product.id %>" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            </div>
            <% }); %>
            <% } else { %>
            <div class="col-12 text-center">
                <p>No products found.</p>
            </div>
        <% } %>
    </div>
</div>

<%- include('footer') %>
C:\mygit\BLazy\repo\nodetest\views\product-detail.ejs
Language detected: python
# filepath: C:\mygit\BLazy\repo\nodetest\views\product.ejs
<%- include('header') %>

<div class="container mt-4">
    <% if (product) { %>
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/">Home</a></li>
                <li class="breadcrumb-item"><a href="/products">Products</a></li>
                <li class="breadcrumb-item active" aria-current="page"><%= product.name %></li>
            </ol>
        </nav>

            <div class="row">
                <div class="col-md-6">
                       <img src="/images/sweater_placeholder.png" class="img-fluid" alt="<%= product.name %>" style="max-height: 400px; object-fit: cover;">
                </div>
                    <div class="col-md-6">
                        <h1><%= product.name %></h1>
                         <p class="lead">Price: $<%= product.price %></p>
                            <p><%= product.description %></p>   
                            
                            <div class="mb-3">
                                <label for="sizeSelect" class="form-label">Size:</label>
                                <select class="form-select"  id="sizeSelect">
                                    <option value="S">Small</option>
                                    <option value="M">Medium</option>
                                    <option value="L">Large</option>
                                    <option value="XL">Extra Large</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="quantitySelect" class="form-label">Quantity:</label>
                                <input type="number" class="form-control" id="quantitySelect" value="1" min="1">
                            </div> 
                            <button class="btn btn-primary">Add to Cart</button>

                            <hr class="my-4">
                            <p><strong>Material:</strong> Wool and Cotton blend</p>   
                            <p><strong>Care Instructions:</strong> Hand wash recommended</p>
                    </div>
            </div>
            <div class="mt-5">
                <h2>Related Products</h2>
                  <div class="row">
                    <% let relatedProducts = [
                        { id: 1, name: 'Classic Wool Sweater', price: 79.99, description: 'A timeless wool sweater for all occasions.' },
                        { id: 2, name: 'Cozy Knit Cardigan', price: 69.99, description: 'A comfortable knitted cardigan perfect for chilly evenings.' },
                        { id: 3, name: 'Stylish Turtleneck Sweater', price: 89.99, description: 'A fashionable turtleneck sweater to keep you warm and stylish.' }
                    ];

                     relatedProducts.forEach(relatedProduct => { %>
                        <div class="col-md-4 mb-4">
                                <div class="card h-100">
                                       <img src="/images/sweater_placeholder.png" class="card-img-top" alt="<%= relatedProduct.name %>" style="height: 200px; object-fit: cover;">
                                    <div class="card-body">
                                        <h5 class="card-title"><%= relatedProduct.name %></h5>
                                        <p class="card-text">Price: $<%= relatedProduct.price %></p>
                                          <a href="/product/<%= relatedProduct.id %>" class="btn btn-primary">View Details</a>
                                    </div>
                                </div>
                            </div>
                    <% }); %>
                 </div>
            </div>
                <div class="mt-5">
                    <h2>Customer Reviews</h2>
                    <p>No reviews yet.</p>
                </div>
                <div class="text-center mt-4">
                    <a href="/products" class="btn btn-secondary">Back to Products</a>
                </div>
        <% } else { %>
        <div class="alert alert-danger text-center">
            Product not found.
        </div>
        <% } %>
        
  </div>


<%- include('footer') %>
C:\mygit\BLazy\repo\nodetest\data\products.js
Language detected: javascript
// filepath: C:\mygit\BLazy\repo\nodetest\products.js
module.exports = [
    {
        id: 1,
        name: 'Classic Wool Sweater',
        price: 79.99,
        description: 'A timeless wool sweater for all occasions.',
        detailedDescription: 'This classic wool sweater is made from 100% fine merino wool, providing exceptional warmth and comfort. Its simple yet elegant design makes it a versatile addition to any wardrobe.',
        imageUrl: '/images/classic_wool_sweater.jpg',
        availableSizes: ['S', 'M', 'L', 'XL'],
        colors: ['Charcoal', 'Navy', 'Heather Gray'],
        material: '100% Merino Wool',
        careInstructions: 'Hand wash cold, lay flat to dry',
        featured: true,
        categories: ['Wool', 'Classic'],
     reviewRatings: 4.5,
        stockStatus: 'In Stock',
    relatedProducts: [2, 3, 4]

    },
    {
        id: 2,
        name: 'Cozy Knit Cardigan',
        price: 69.99,
        description: 'A comfortable knitted cardigan perfect for chilly evenings.',
       detailedDescription: 'The Cozy Knit Cardigan is made from a soft blend of cotton and acrylic. It features a relaxed fit with open front, making it perfect for layering. Ideal for those cooler nights.',
        imageUrl: '/images/cozy_knit_cardigan.jpg',
        availableSizes: ['S', 'M', 'L', 'XL', 'XXL'],
        colors: ['Beige', 'Light Pink', 'Cream'],
        material: '50% Cotton, 50% Acrylic',
        careInstructions: 'Machine wash cold, tumble dry low',
        featured: false,
        categories: ['Cardigan', 'Knit'],
          reviewRatings: 4.2,
           stockStatus: 'In Stock',
     relatedProducts: [1, 3, 5]
    },
    {
        id: 3,
        name: 'Stylish Turtleneck Sweater',
        price: 89.99,
        description: 'A fashionable turtleneck sweater to keep you warm and stylish.',
       detailedDescription: 'This stylish turtleneck sweater is crafted from a blend of cashmere and silk, offering supreme softness and warmth. Its slim fit is perfect for layering or wearing on its own.',
        imageUrl: '/images/stylish_turtleneck_sweater.jpg',
        availableSizes: ['XS', 'S', 'M', 'L'],
        colors: ['Black', 'Burgundy', 'Forest Green'],
        material: '70% Cashmere, 30% Silk',
        careInstructions: 'Dry clean only',
        featured: true,
        categories: ['Turtleneck', 'Luxury'],
         reviewRatings: 4.8,
        stockStatus: 'Low Stock',
           relatedProducts: [1, 2, 6]
    },
    {
        id: 4,
        name: 'Lightweight Cotton Sweater',
        price: 59.99,
         description: 'A soft and light cotton sweater, ideal for layering.',
        detailedDescription: 'The Lightweight Cotton Sweater is made from 100% organic cotton, offering a breathable and comfortable fit. Its versatile design makes it perfect for everyday wear.',
        imageUrl: '/images/lightweight_cotton_sweater.jpg',
        availableSizes: ['S', 'M', 'L', 'XL', 'XXL'],
        colors: ['White', 'Light Blue', 'Gray'],
        material: '100% Organic Cotton',
        careInstructions: 'Machine wash cold, tumble dry low',
        featured: false,
         reviewRatings: 4.0,
        stockStatus: 'In Stock',
           relatedProducts: [1, 5, 7]
    },
      {
        id: 5,
        name: 'Hooded Fleece Sweater',
        price: 64.99,
         description: 'A comfortable fleece sweater for casual wear.',
          detailedDescription: 'The Hooded Fleece Sweater is perfect for staying warm and cozy on a relaxed weekend. Made from soft and durable fleece material, it features a comfortable hood and kangaroo pocket.',
        imageUrl: '/images/hooded_fleece_sweater.jpg',
        availableSizes: ['S', 'M', 'L', 'XL'],
        colors: ['Navy', 'Charcoal', 'Dark Green'],
        material: '100% Polyester Fleece',
         careInstructions: 'Machine wash cold, tumble dry low',
        featured: false,
       reviewRatings: 4.3,
        stockStatus: 'In Stock',
          relatedProducts: [2, 4, 8]
    },
     {
        id: 6,
        name: 'Ribbed Merino Wool Sweater',
        price: 99.99,
         description: 'A premium ribbed sweater with a stylish design.',
           detailedDescription: 'This Ribbed Merino Wool Sweater is designed to provide both sophisticated style and warmth. It is made from a high-quality merino wool and features a classic ribbed pattern.',
         imageUrl: '/images/ribbed_merino_wool_sweater.jpg',
        availableSizes: ['XS', 'S', 'M', 'L'],
        colors: ['Camel', 'Black', 'Grey'],
        material: '100% Merino Wool',
         careInstructions: 'Hand wash cold, lay flat to dry',
        featured: true,
   reviewRatings: 4.7,
        stockStatus: 'In Stock',
           relatedProducts: [3, 7, 9]
    },
    {
        id: 7,
        name: 'Cotton Blend Pullover',
        price: 49.99,
        description: 'A simple and versatile cotton blend pullover.',
           detailedDescription: 'This Cotton Blend Pullover is designed for everyday comfort and style. The material consists of a blend of  cotton and polyester that is soft and durable for daily wear.',
        imageUrl: '/images/cotton_blend_pullover.jpg',
        availableSizes: ['S', 'M', 'L', 'XL', 'XXL'],
        colors: ['Light Blue', 'Navy', 'Red'],
        material: '60% Cotton, 40% Polyester',
        careInstructions: 'Machine wash cold, tumble dry low',
        featured: false,
  reviewRatings: 4.1,
        stockStatus: 'In Stock',
           relatedProducts: [4, 6, 10]
    },
     {
        id: 8,
        name: 'Oversized Cable Knit Sweater',
        price: 84.99,
         description: 'An oversized stylish cable knit sweater',
           detailedDescription: 'This Oversized Cable Knit Sweater is perfect for those who love a relaxed and cozy fit. Made from a blend of acrylic and wool. It is stylish and comfortable.',
         imageUrl: '/images/oversized_cable_knit_sweater.jpg',
        availableSizes: ['S', 'M', 'L', 'XL'],
        colors: ['Cream', 'Beige', 'Light Grey'],
        material: '60% Acrylic, 40% Wool',
         careInstructions: 'Hand wash cold, lay flat to dry',
        featured: true,
 reviewRatings: 4.6,
        stockStatus: 'In Stock',
           relatedProducts: [5, 9, 1]
    },
     {
        id: 9,
        name: 'Cashmere V-Neck Sweater',
        price: 129.99,
         description: 'A luxurious cashmere V-neck sweater.',
            detailedDescription: 'This Cashmere V-Neck Sweater is made from 100% pure cashmere, providing ultimate softness and warmth. It features a classic V-neck design suitable for both casual and formal occasions.',
         imageUrl: '/images/cashmere_v_neck_sweater.jpg',
        availableSizes: ['XS', 'S', 'M', 'L'],
        colors: ['Black', 'Charcoal', 'Navy'],
        material: '100% Cashmere',
        careInstructions: 'Dry clean only',
         featured: false,
       reviewRatings: 4.9,
        stockStatus: 'In Stock',
           relatedProducts: [6, 8, 2]
    },
      {
        id: 10,
        name: 'Striped Crew Neck Sweater',
        price: 54.99,
         description: 'A comfortable and classic striped crew neck sweater.',
       detailedDescription: 'This Striped Crew Neck Sweater is a stylish option for any casual occasion. Made from a soft cotton blend, it features a timeless striped design and a classic crew neck.',
         imageUrl: '/images/striped_crew_neck_sweater.jpg',
        availableSizes: ['S', 'M', 'L', 'XL', 'XXL'],
        colors: ['Navy/White', 'Red/White', 'Black/Gray'],
        material: '70% Cotton, 30% Polyester',
         careInstructions: 'Machine wash cold, tumble dry low',
        featured: false,
  reviewRatings: 4.2,
        stockStatus: 'In Stock',
           relatedProducts: [7, 1, 3]
    }
];
