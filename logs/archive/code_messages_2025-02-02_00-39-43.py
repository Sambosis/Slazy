C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
const express = require('express');
const path = require('path');

const app = express();
const port = 3000;

// Set EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Basic array of sweater products
const products = [
    {
        id: 1,
        name: 'Cozy Knit Sweater',
        description: 'A warm and comfortable knit sweater for chilly days.',
        price: 49.99,
        image: '/images/sweater1.jpg'
    },
    {
        id: 2,
        name: 'Classic Crewneck Sweater',
        description: 'A timeless crewneck sweater perfect for any occasion.',
        price: 39.99,
        image: '/images/sweater2.jpg'
    },
    {
        id: 3,
        name: 'Stylish V-Neck Sweater',
        description: 'A fashionable V-neck sweater that will elevate your style.',
        price: 59.99,
        image: '/images/sweater3.jpg'
    }
];


// Routes
app.get('/', (req, res) => {
    res.render('index', { title: 'Sweater Store' });
});

app.get('/products', (req, res) => {
    res.render('products', { title: 'Products', products: products });
});

app.get('/product/:id', (req, res) => {
    const productId = parseInt(req.params.id);
    const product = products.find(p => p.id === productId);

    if (product) {
        res.render('product', { title: product.name, product: product });
    } else {
        res.status(404).send('Product not found');
    }
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
    <title><%- title %></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Sweater Store</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
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

    <div class="container my-4">
        <%- body %>
    </div>

    <footer class="bg-light text-center py-3">
        <div class="container">
            <p>&copy; 2023 Sweater Store. All rights reserved.</p>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
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
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Sweater Store</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
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

    <div class="container my-4">
        <section class="hero text-center py-5">
            <div class="container">
                <h1 class="display-4">Welcome to Our Sweater Store</h1>
                <p class="lead">Find the perfect cozy sweater for any occasion.</p>
                <div class="row justify-content-center mt-4">
                     <div class="col-md-6">
                        <img src="/images/sweater1.jpg" alt="Featured Sweater" class="img-fluid rounded">
                    </div>
                    <div class="col-md-6 text-start">
                         <h2 class="mt-3">Cozy Knit Sweater</h2>
                        <p>A warm and comfortable knit sweater for chilly days.</p>
                        <p class="fw-bold">$49.99</p>
                        <a href="/product/1" class="btn btn-primary">Shop Now</a>
                    </div>
                </div>
            </div>
        </section>

        <section class="featured-products py-5">
            <div class="container">
                <h2 class="text-center mb-4">Featured Products</h2>
                 <div class="row">
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            <img src="/images/sweater1.jpg" class="card-img-top" alt="Cozy Knit Sweater">
                            <div class="card-body">
                                <h5 class="card-title">Cozy Knit Sweater</h5>
                                <p class="card-text">A warm and comfortable knit sweater for chilly days.</p>
                                 <p class="fw-bold">$49.99</p>
                                <a href="/product/1" class="btn btn-primary">Shop Now</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            <img src="/images/sweater2.jpg" class="card-img-top" alt="Classic Crewneck Sweater">
                            <div class="card-body">
                                <h5 class="card-title">Classic Crewneck Sweater</h5>
                                <p class="card-text">A timeless crewneck sweater perfect for any occasion.</p>
                                 <p class="fw-bold">$39.99</p>
                                <a href="/product/2" class="btn btn-primary">Shop Now</a>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4">
                        <div class="card">
                            <img src="/images/sweater3.jpg" class="card-img-top" alt="Stylish V-Neck Sweater">
                            <div class="card-body">
                                <h5 class="card-title">Stylish V-Neck Sweater</h5>
                                <p class="card-text">A fashionable V-neck sweater that will elevate your style.</p>
                                <p class="fw-bold">$59.99</p>
                                <a href="/product/3" class="btn btn-primary">Shop Now</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
           <section class="why-choose-us py-5 bg-light">
            <div class="container">
                <h2 class="text-center mb-4">Why Choose Us</h2>
                <div class="row text-center">
                    <div class="col-md-4 mb-3">
                        <h4>High-Quality Materials</h4>
                        <p>We use only the finest materials to ensure your sweaters are both comfortable and durable.</p>
                    </div>
                    <div class="col-md-4 mb-3">
                        <h4>Stylish Designs</h4>
                         <p>Our sweaters are designed to keep you looking fashionable for any event.</p>
                    </div>
                    <div class="col-md-4 mb-3">
                         <h4>Exceptional Customer Service</h4>
                        <p>Our team is dedicated to providing you top level service.</p> 
                    </div>
                       
                </div>
            </div>
        </section>
    </div>

    <footer class="bg-light text-center py-3">
        <div class="container">
            <p>&copy; 2023 Sweater Store. All rights reserved.</p>
        </div>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\views\products.ejs
Language detected: ejs
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%- title %></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <%- include('layout', { body: body, title: title }) %>
    <div class="container my-4">
        <header class="mb-4">
            <h1>Our Sweater Collection</h1>
        </header>
        
        <section class="mb-4">
             <div class="row mb-3">
                <div class="col-md-6">
                    <div class="d-flex">
                       <select class="form-select" aria-label="Default select example" style="width:auto">
                          <option selected>Sort By</option>
                          <option value="1">Price: Low to High</option>
                          <option value="2">Price: High to Low</option>
                          <option value="3">Name: A to Z</option>
                        </select>
                    </div>
                </div>
            </div>
        </section>

        <section class="products">
            <div class="row">
                <% products.forEach(product => { %>
                    <div class="col-sm-6 col-md-4 col-lg-3 mb-4">
                        <div class="card">
                            <img src="<%= product.image %>" class="card-img-top" alt="<%= product.name %>">
                            <div class="card-body">
                                <h5 class="card-title"><%= product.name %></h5>
                                <p class="card-text"><%= product.description %></p>
                                <p class="fw-bold">$<%= product.price %></p>
                                <a href="/product/<%= product.id %>" class="btn btn-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                <% }); %>
            </div>
        </section>
           <nav aria-label="Page navigation">
            <ul class="pagination justify-content-center">
                <li class="page-item disabled">
                    <a class="page-link" href="#" tabindex="-1" aria-disabled="true">Previous</a>
               </li>
                <li class="page-item active" aria-current="page">
                    <a class="page-link" href="#">1</a>
                </li>
                <li class="page-item">
                     <a class="page-link" href="#">2</a>
                 </li>
                <li class="page-item">
                     <a class="page-link" href="#">3</a>
                 </li>
                <li class="page-item">
                    <a class="page-link" href="#">Next</a>
               </li>
           </ul>
        </nav>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\views\product-detail.ejs
Language detected: ejs
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%- title %></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/styles.css">
</head>
<body>
    <%- include('layout', { body: body, title: title }) %>

    <div class="container my-4">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/">Home</a></li>
                <li class="breadcrumb-item"><a href="/products">Products</a></li>
                <li class="breadcrumb-item active" aria-current="page"><%- product.name %></li>
            </ol>
        </nav>


        <section class="product-details mb-5">
            <div class="row">
                <div class="col-md-6">
                    <img src="<%- product.image %>" alt="<%- product.name %>" class="img-fluid rounded">
                </div>
                <div class="col-md-6">
                    <h2 class="display-5"><%- product.name %></h2>
                    <p class="lead fw-bold">$<%- product.price %></p>
                    <p class="mb-4"><%- product.description %></p>

                    <div class="mb-3">
                        <label for="sizeSelector" class="form-label">Size</label>
                        <select class="form-select" id="sizeSelector">
                            <option value="S">S</option>
                            <option value="M">M</option>
                            <option value="L">L</option>
                            <option value="XL">XL</option>
                        </select>
                    </div>

                   <div class="mb-3">
                        <label for="quantitySelector" class="form-label">Quantity</label>
                        <input type="number" class="form-control" id="quantitySelector" value="1" min="1">
                    </div>

                    <button class="btn btn-primary">Add to Cart</button>
                </div>
            </div>
        </section>

        <section class="product-features mb-5">
            <h3>Product Features</h3>
            <ul class="list-unstyled">
                <li><strong>Material:</strong> 100% Cotton</li>
                <li><strong>Care Instructions:</strong> Machine wash cold, tumble dry low</li>
                <li><strong>Fit:</strong> Relaxed fit</li>
                <li><strong>Origin:</strong> Imported</li>
            </ul>
        </section>

         <section class="related-products">
            <h3 class="mb-4">You May Also Like</h3>
             <div class="row">
                <div class="col-sm-6 col-md-4 mb-4">
                    <div class="card">
                        <img src="/images/sweater2.jpg" class="card-img-top" alt="Classic Crewneck Sweater">
                         <div class="card-body">
                            <h5 class="card-title">Classic Crewneck Sweater</h5>
                             <p class="card-text">A timeless crewneck sweater perfect for any occasion.</p>
                              <p class="fw-bold">$39.99</p>
                         <a href="/product/2" class="btn btn-primary">View Details</a>
                      </div>
                   </div>
                </div>
                <div class="col-sm-6 col-md-4 mb-4">
                     <div class="card">
                        <img src="/images/sweater3.jpg" class="card-img-top" alt="Stylish V-Neck Sweater">
                        <div class="card-body">
                             <h5 class="card-title">Stylish V-Neck Sweater</h5>
                             <p class="card-text">A fashionable V-neck sweater that will elevate your style.</p>
                             <p class="fw-bold">$59.99</p>
                             <a href="/product/3" class="btn btn-primary">View Details</a>
                       </div>
                    </div>
                </div>
                <div class="col-sm-6 col-md-4 mb-4">
                    <div class="card">
                        <img src="/images/sweater1.jpg" class="card-img-top" alt="Cozy Knit Sweater">
                            <div class="card-body">
                                 <h5 class="card-title">Cozy Knit Sweater</h5>
                                <p class="card-text">A warm and comfortable knit sweater for chilly days.</p>
                                  <p class="fw-bold">$49.99</p>
                                <a href="/product/1" class="btn btn-primary">View Details</a>
                          </div>
                      </div>
                </div>
            </div>
        </section>



    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\data\products.js
Language detected: javascript
// filepath: C:\mygit\BLazy\repo\nodetest\data\products.js
module.exports = [
    {
        id: 1,
        name: 'Cozy Knit Cardigan',
        shortDescription: 'A warm and comfortable knit cardigan.',
        description: 'Wrap yourself in our Cozy Knit Cardigan, perfect for layering on chilly days. This cardigan features a relaxed fit, long sleeves, and open front.',
        price: 59.99,
        availableSizes: ['S', 'M', 'L', 'XL'],
        image: '/images/cardigan1.jpg',
        features: ['Relaxed fit', 'Open front', 'Long sleeves'],
        careInstructions: 'Machine wash cold, tumble dry low.',
        material: '50% Cotton, 50% Acrylic',
        categories: ['cardigan', 'knitwear', 'casual'],
        featured: true
    },
    {
        id: 2,
        name: 'Classic Pullover Sweater',
        shortDescription: 'A timeless crewneck pullover.',
        description: 'Our Classic Pullover Sweater is a wardrobe staple, perfect for any occasion. Its classic crewneck design offers timeless style and comfort.',
        price: 49.99,
        availableSizes: ['XS', 'S', 'M', 'L', 'XL'],
        image: '/images/pullover1.jpg',
        features: ['Crewneck', 'Long sleeves', 'Ribbed cuffs and hem'],
        careInstructions: 'Machine wash cold, tumble dry low.',
        material: '100% Cotton',
        categories: ['pullover', 'casual', 'basic'],
        featured: false
    },
    {
        id: 3,
        name: 'Elegant Turtleneck Sweater',
        shortDescription: 'A stylish turtleneck sweater.',
        description: 'Elevate your look with our Elegant Turtleneck Sweater. This sophisticated sweater features a high neckline and slim fit, perfect for both casual and dressy occasions.',
        price: 69.99,
        availableSizes: ['S', 'M', 'L'],
        image: '/images/turtleneck1.jpg',
        features: ['Turtleneck', 'Slim fit', 'Long sleeves'],
         careInstructions: 'Hand wash recommended.',
        material: '70% Merino Wool, 30% Cashmere',
        categories: ['turtleneck', 'formal', 'winter'],
        featured: true
    },
    {
        id: 4,
        name: 'Chunky Cable Knit Sweater',
          shortDescription: 'A cozy and warm cable knit sweater.',
        description: 'Stay warm and stylish with our Chunky Cable Knit Sweater. This sweater boasts chunky knit details and a relaxed fit for ultimate comfort.',
        price: 79.99,
        availableSizes: ['M', 'L', 'XL'],
        image: '/images/cableknit1.jpg',
        features: ['Cable knit design', 'Chunky knit', 'Relaxed fit'],
        careInstructions: 'Machine wash cold, lay flat to dry',
        material: '100% Acrylic',
           categories: ['cable knit', 'winter', 'casual'],
            featured: false
    },
     {
        id: 5,
        name: 'Lightweight V-Neck Sweater',
        shortDescription: 'A lightweight v neck perfect for layering',
        description: 'Our Lightweight V-Neck Sweater is great for layering or wearing alone. Perfect for any season with a stylish V Neck design.',
        price: 44.99,
        availableSizes: ['XS', 'S', 'M', 'L', 'XL','XXL'],
        image: '/images/vneck1.jpg',
        features: ['V-neck', 'Lightweight', 'Long sleeves'],
        careInstructions: 'Machine wash cold, tumble dry low.',
        material: '60% Cotton, 40% Polyester',
        categories: ['v-neck', 'casual', 'layering'],
         featured: false
    },
      {
        id: 6,
        name: 'Bohemian Patterned Cardigan',
        shortDescription: 'A stylish patterned cardigan with a bohemian feel',
        description: 'Add style to your outfit with our Bohemian Patterned Cardigan. Its unique pattern and relaxed fit will make your outfit pop.',
        price: 64.99,
       availableSizes: ['S', 'M', 'L','XL'],
        image: '/images/patternedcardigan1.jpg',
        features: ['Open front', 'Patterned knit', 'Relaxed fit'],
        careInstructions: 'Hand wash cold, hang dry',
        material: '60% Viscose, 40% Acrylic',
        categories: ['cardigan', 'bohemian', 'fashion'],
          featured: true
    },
    {
        id: 7,
        name: 'Striped Mock Neck Sweater',
           shortDescription: 'A modern mock neck sweater with a striped design',
        description: 'Stay on top of the latest styles with our Striped Mock Neck Sweater. Its unique high neck design and striping is perfect for casual and stylish looks.',
        price: 54.99,
         availableSizes: ['S', 'M', 'L'],
        image: '/images/mockneck1.jpg',
          features: ['Mock neck', 'Striped design', 'Long sleeves'],
        careInstructions: 'Machine wash cold, lay flat to dry',
        material: '100% Cotton',
           categories: ['mock neck', 'casual', 'stripes'],
            featured: false
    },
     {
        id: 8,
        name: 'Oversized Knit Poncho',
           shortDescription: 'A comfortable and oversized knit poncho ',
        description: 'Our Oversized Knit Poncho will give you comfort and style like no other. Its unique poncho design will keep you warm and comfortable.',
        price: 89.99,
        availableSizes: ['One Size'],
        image: '/images/poncho1.jpg',
          features: ['Oversized design', 'Knit pattern', 'Comfortable'],
            careInstructions: 'Hand wash cold, lay flat to dry',
        material: '70% Acrylic, 30% Wool ',
           categories: ['poncho', 'oversized', 'casual'],
             featured: true
    }
];
C:\mygit\BLazy\repo\nodetest\utils\middleware.js
Language detected: javascript
// filepath: C:\mygit\BLazy\repo\nodetest\middleware\utils.js
const productsData = require('../data/products');

// Error handling middleware
const errorHandler = (err, req, res, next) => {
    console.error(err.stack);

    if (res.headersSent) {
        return next(err);
    }
    
    if(err.message === "Product not found") {
        res.status(404).send("Product not found")
        return;
    }

    // Handle specific errors
    const statusCode = res.statusCode === 200 ? 500 : res.statusCode;
    res.status(statusCode);
    res.render('error', { title: 'Error', message: 'Oops! Something went wrong on our end.' });

};


// 404 Not Found Error Handler
const notFoundHandler = (req, res) => {
  res.status(404);

    res.render('error', { title: 'Not Found', message: 'Oops! Page not found' });
};


// Request logging middleware
const requestLogger = (req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);
    next();
};


// Helper function: Product filtering
const filterProducts = (products, filters) => {
    if (!filters || Object.keys(filters).length === 0) {
        return products;
    }

    return products.filter(product => {
        for (const key in filters) {
            if (filters.hasOwnProperty(key)) {
                const filterValue = filters[key];
                if(filterValue){
                  if(key === "price"){
                        let [minPrice, maxPrice] = filterValue.split('-').map(Number);
                        if(maxPrice){
                           if(product.price < minPrice || product.price > maxPrice){
                               return false
                            }
                        } else {
                            if(product.price < minPrice){
                              return false;
                            }
                        }
                      
                   } else if (Array.isArray(filterValue)) {
                      if (!filterValue.includes(product[key])) {
                          return false;
                      }
                 } else if(typeof product[key] === 'string'){
                     if(filterValue && !product[key].toLowerCase().includes(filterValue.toLowerCase())){
                            return false;
                      }
                 } else if (product[key] !== filterValue) {
                      return false;
                    }
                }
            }
        }
        return true;
    });
};

// Helper function: Price formatting
const formatPrice = (price) => {
    return `$${price.toFixed(2)}`;
};

//Helper function: Size Validation
const validateSize = (size, availableSizes) => {
    if(!availableSizes || availableSizes.length === 0 )
    {
        return true
    }
    if(!size){
         return true;
    }
    return availableSizes.includes(size.toUpperCase());
};

// Helper function: Related products finder
const findRelatedProducts = (productId, products, limit = 3) => {
    const product = products.find(p => p.id === productId);
    if (!product) {
        return [];
    }

    const relatedProducts = products.filter(p =>
      p.id !== productId && p.categories.some(category => product.categories.includes(category))
    );


    return relatedProducts.slice(0,limit);
};
module.exports = {
    errorHandler,
    requestLogger,
  notFoundHandler,
    filterProducts,
    formatPrice,
    validateSize,
    findRelatedProducts
};
