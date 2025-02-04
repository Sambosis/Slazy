C:\mygit\BLazy\repo\nodetest\app.js
Language detected: python
# No python code needed here. Since the problem specifies a Node.js server, this response contains Javascript code
# which is to be run in a Node.js environment, not Python

# server.js
const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const port = 3000;

// Set up EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Serve static files from the 'public' directory
app.use(express.static(path.join(__dirname, 'public')));

// Use body-parser for parsing request bodies
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());


// Sample sweater data
const sweaters = [
    {
        id: 1,
        name: 'Classic Crewneck',
        description: 'A timeless, comfortable crewneck sweater.',
        price: 49.99,
        imageUrl: '/images/crewneck.jpg'
    },
      {
        id: 2,
        name: 'Cozy Cardigan',
        description: 'A warm and stylish cardigan for layering.',
        price: 59.99,
        imageUrl:'/images/cardigan.jpg'
    },
    {
        id: 3,
        name: 'Striped Pullover',
        description: 'A trendy striped pullover sweater.',
        price: 54.99,
        imageUrl: '/images/striped.jpg'
    },
    {
      id: 4,
      name: 'Wool Turtleneck',
      description: 'A warm and elegant wool turtleneck for winter.',
      price: 69.99,
      imageUrl: '/images/turtleneck.jpg'
    }
];

// Routes
app.get('/', (req, res) => {
    res.render('home', { pageTitle: 'Home' });
});

app.get('/products', (req, res) => {
    res.render('products', { pageTitle: 'Products', sweaters: sweaters });
});

app.get('/products/:id', (req, res) => {
    const productId = parseInt(req.params.id);
    const sweater = sweaters.find(s => s.id === productId);
    if (sweater) {
      res.render('product', { pageTitle: sweater.name, sweater: sweater});
    }else{
        res.status(404).send('Sweater not found')
    }
    
});

// Start the server
app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\layout.ejs
Language detected: ejs
<!-- views/layout.ejs -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%= pageTitle %></title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="/">Sweater Store</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav">
            <li class="nav-item active">
              <a class="nav-link" href="/">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/products">Products</a>
            </li>
          </ul>
        </div>
      </nav>

    <div class="container mt-4">
        <%- body %>
    </div>

    <footer class="mt-5 text-center py-3 bg-light">
        <p>&copy; <%= new Date().getFullYear() %> Sweater Store. All rights reserved.</p>
    </footer>

    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.3/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\views\index.ejs
Language detected: html
<!-- views/home.ejs -->
<%- include('layout') %>

<div class="jumbotron text-center">
    <h1 class="display-4">Welcome to the Sweater Store</h1>
    <p class="lead">Find your perfect sweater for any occasion.</p>
    <img src="/images/hero-sweater.jpg" alt="Featured Sweater" class="img-fluid rounded mb-3" style="max-height: 300px;">
    <a href="/products" class="btn btn-primary btn-lg">Shop Now</a>
</div>

<div class="container">
    <section class="mb-5">
        <h2>Special Offers</h2>
        <div class="alert alert-info" role="alert">
            Get 15% off your first purchase! Use code NEW15 at checkout.
        </div>
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                  <img src="/images/sale-sweater-1.jpg" alt="Special Offer 1" class="card-img-top" style="max-height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h5 class="card-title">Limited Time Offer</h5>
                        <p class="card-text">Selected sweaters are now 20% off.</p>
                    </div>
                </div>
            </div>
              <div class="col-md-6">
                <div class="card">
                  <img src="/images/sale-sweater-2.jpg" alt="Special Offer 2" class="card-img-top" style="max-height: 200px; object-fit: cover;">
                    <div class="card-body">
                        <h5 class="card-title">Bundle Deal</h5>
                        <p class="card-text">Buy two sweaters, get the third for 50% off!</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section class="mb-5">
        <h2>Featured Sweaters</h2>
        <div class="row row-cols-1 row-cols-md-3 g-4">
            <div class="col">
              <div class="card h-100">
                <img src="/images/crewneck.jpg" class="card-img-top" alt="Crewneck Sweater" style="max-height: 250px; object-fit: cover;">
                <div class="card-body">
                  <h5 class="card-title">Classic Crewneck</h5>
                    <p class="card-text">A timeless and versatile style.</p>
                    <a href="/products/1" class="btn btn-outline-primary">View Details</a>
                </div>
              </div>
            </div>
            <div class="col">
                <div class="card h-100">
                  <img src="/images/cardigan.jpg" class="card-img-top" alt="Cardigan Sweater" style="max-height: 250px; object-fit: cover;">
                  <div class="card-body">
                    <h5 class="card-title">Cozy Cardigan</h5>
                    <p class="card-text">Perfect for layering on chilly days.</p>
                    <a href="/products/2" class="btn btn-outline-primary">View Details</a>
                  </div>
                </div>
            </div>
              <div class="col">
                <div class="card h-100">
                  <img src="/images/striped.jpg" class="card-img-top" alt="Striped Pullover" style="max-height: 250px; object-fit: cover;">
                  <div class="card-body">
                    <h5 class="card-title">Striped Pullover</h5>
                    <p class="card-text">Bring a pop of design to your wardrobe.</p>
                    <a href="/products/3" class="btn btn-outline-primary">View Details</a>
                 </div>
                </div>
            </div>
        </div>
        
    </section>

    <div class="text-center">
        <a href="/products" class="btn btn-primary btn-lg">See All Sweaters</a>
    </div>
</div>
C:\mygit\BLazy\repo\nodetest\views\products.ejs
Language detected: html
<!-- views/products.ejs -->
<%- include('layout') %>

<div class="container">
    <h1>All Sweaters</h1>

    <div class="row">
        <div class="col-md-3">
            <div class="mb-4">
                <h3>Filter</h3>
                <div class="card p-3">
                  <div class="mb-3">
                      <label for="categoryFilter" class="form-label">Category</label>
                      <select id="categoryFilter" class="form-select">
                          <option value="">All</option>
                          <option value="crewneck">Crewneck</option>
                          <option value="cardigan">Cardigan</option>
                           <option value="pullover">Pullover</option>
                            <option value="turtleneck">Turtleneck</option>
                      </select>
                  </div>
                    <div class="mb-3">
                       <label for="minPrice" class="form-label">Min Price:</label>
                        <input type="number" class="form-control" id="minPrice" placeholder="Enter min price">
                    </div>
                    <div class="mb-3">
                       <label for="maxPrice" class="form-label">Max Price:</label>
                        <input type="number" class="form-control" id="maxPrice" placeholder="Enter max price">
                   </div>
                    <button id="applyFilters" class="btn btn-primary">Apply Filters</button>
                     <button id="clearFilters" class="btn btn-secondary">Clear Filters</button>
                </div>
               
            </div>
             <div class="mb-4">
                <h3>Sort By</h3>
                <div class="card p-3">
                    <div class="mb-2">
                        <select id="sortOptions" class="form-select">
                            <option value="default">Default</option>
                             <option value="price-low-high">Price: Low to High</option>
                            <option value="price-high-low">Price: High to Low</option>
                            <option value="newest">Newest</option>
                        </select>
                    </div>
                     <button id="applySort" class="btn btn-primary">Apply Sort</button>
                </div>
            </div>
        </div>
        <div class="col-md-9">
              <div id="product-grid" class="row row-cols-1 row-cols-md-3 g-4">
                <% sweaters.forEach(sweater => { %>
                    <div class="col">
                        <div class="card h-100">
                            <img src="<%= sweater.imageUrl %>" alt="<%= sweater.name %>" class="card-img-top" style="max-height: 250px; object-fit: cover;">
                            <div class="card-body">
                                <h5 class="card-title"><%= sweater.name %></h5>
                                <p class="card-text"><%= sweater.description %></p>
                                <p class="card-text"><strong>Price:</strong> $<%= sweater.price %></p>
                                <a href="/products/<%= sweater.id %>" class="btn btn-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                <% }); %>
             </div>

             <nav aria-label="Page navigation" class="mt-4">
                  <ul id="pagination" class="pagination justify-content-center">
                    <!-- Pagination links will be generated here -->
                   </ul>
            </nav>
          <div id="no-results"  class="alert alert-info d-none" role="alert">
            No results found. Please adjust your filters
         </div>
        </div>
    </div>
</div>


<script>
     document.addEventListener('DOMContentLoaded', () => {


    const sweaters =  <%= JSON.stringify(sweaters) %>; // Get products form server
    const productGrid =  document.getElementById('product-grid');
     const paginationContainer = document.getElementById('pagination');
     const noResultsAlert = document.getElementById('no-results');
    const itemsPerPage = 6;
    let currentPage = 1;
    let filteredSweaters = [...sweaters]; // use copy of original array
   
    function renderProducts(products) {
      productGrid.innerHTML = ''; // clear the product grid
            if(products.length === 0) {
               noResultsAlert.classList.remove('d-none');
               return;
             }else {
               noResultsAlert.classList.add('d-none');
           }
            products.forEach(sweater => {
                const productCard =  `
                    <div class="col">
                        <div class="card h-100">
                            <img src="${sweater.imageUrl}" alt="${sweater.name}" class="card-img-top" style="max-height: 250px; object-fit: cover;">
                            <div class="card-body">
                                <h5 class="card-title">${sweater.name}</h5>
                                 <p class="card-text">${sweater.description}</p>
                                <p class="card-text"><strong>Price:</strong> $${sweater.price}</p>
                                <a href="/products/${sweater.id}" class="btn btn-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                    `;
                     productGrid.innerHTML += productCard;
      });

   }

       function renderPagination(totalItems) {
           paginationContainer.innerHTML = '';
           const totalPages = Math.ceil(totalItems / itemsPerPage)

           for(let i = 1; i <= totalPages; i++) {
               const li = document.createElement('li');
               li.classList.add('page-item');
               if(i === currentPage){
                   li.classList.add('active')
               }

               const link = document.createElement('a');
                link.classList.add('page-link');
                link.href = '#';
                link.innerText = i;
                link.addEventListener('click', () => {

                  currentPage = i;
                    updateProductDisplay();
                });


               li.appendChild(link);
                paginationContainer.appendChild(li);
           }

        }

    function updateProductDisplay(){
         const startIndex = (currentPage - 1) * itemsPerPage;
           const endIndex = startIndex + itemsPerPage;
            const paginatedProducts = filteredSweaters.slice(startIndex, endIndex)
            renderProducts(paginatedProducts);
            renderPagination(filteredSweaters.length);
    }

        function applyFilters(){
          const categoryFilter = document.getElementById('categoryFilter').value.toLowerCase();
          const minPrice = parseFloat(document.getElementById('minPrice').value) || 0;
          const maxPrice = parseFloat(document.getElementById('maxPrice').value) || Infinity;  // if no max set to infinity


        filteredSweaters = sweaters.filter((sweater)=>{
          const matchesCategory =  categoryFilter === ''|| sweater.name.toLowerCase().includes(categoryFilter) || sweater.description.toLowerCase().includes(categoryFilter)
        const matchesPrice = sweater.price >= minPrice && sweater.price <= maxPrice;
          return matchesCategory && matchesPrice;
       })

       currentPage = 1 ; // reset to page 1
        updateProductDisplay();
    }


      function applySort () {
        const sortOption = document.getElementById('sortOptions').value;
            switch(sortOption){
              case 'price-low-high':
              filteredSweaters.sort((a,b) => a.price - b.price);
              break;
                  case 'price-high-low':
              filteredSweaters.sort((a,b) => b.price - a.price);
              break;
              case 'newest':
                  // implement if there is date field in data set
                  break;
                default:
                    filteredSweaters = [...sweaters] // reset to original order
                break;
             }
           updateProductDisplay();

      }

        document.getElementById('applyFilters').addEventListener('click', applyFilters);
        document.getElementById('applySort').addEventListener('click', applySort);
         document.getElementById('clearFilters').addEventListener('click', () => {
             document.getElementById('categoryFilter').value = "";
              document.getElementById('minPrice').value = "";
              document.getElementById('maxPrice').value = "";
              filteredSweaters = [...sweaters];
               currentPage = 1;
             updateProductDisplay()

         })


        updateProductDisplay(); // initial page load

     });
</script>
C:\mygit\BLazy\repo\nodetest\public\css\style.css
Language detected: javascript
// filepath: C:\mygit\BLazy\repo\nodetest\public\css\style.css
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --accent-color: #e74c3c;
    --text-color-light: #f8f9fa;
     --text-color-dark: #212529;
    --bg-light: #ecf0f1;
    --bg-dark: #34495e;
    --box-shadow: 0 4px 8px rgba(0,0,0,0.1);
     --border-radius: 5px;
}

body {
    font-family: 'Arial', sans-serif;
    color: var(--text-color-dark);
    background-color: var(--bg-light);
}

/* Navigation bar styling */
.navbar {
    background-color: var(--bg-light);
    box-shadow: var(--box-shadow);
}

.navbar-brand {
    color: var(--primary-color);
    font-weight: bold;
}

.navbar-light .navbar-nav .nav-link {
  color: var(--primary-color); /* Dark text for link */
  transition: color 0.3s; /* Smooth transition on hover */
}

.navbar-light .navbar-nav .nav-link:hover {
    color: var(--secondary-color);
}

.navbar-light .navbar-nav .nav-link.active {
    font-weight: bold;
    color: var(--secondary-color);
}
/* Hero section with overlay */
.jumbotron {
    background-color: var(--bg-light);
    position: relative;
    overflow: hidden;
    color: var(--primary-color);
}

.jumbotron::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(255, 255, 255, 0.3); /* Adjust as needed */
    z-index:1;
}

.jumbotron > * {
    z-index: 2; /* Ensure text and buttons are above the overlay */
    position: relative; /* Required for z-index to work */
}

.jumbotron img{
    z-index: 0;/* Ensure image below the overlay */
    filter: brightness(80%)
}


/* Product card styling and hover effects */
.card {
    border: none;
    box-shadow: var(--box-shadow);
    transition:  0.3s ease;
}
.card:hover {
 transform: translateY(-5px);
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
}
.card-img-top {
    border-top-left-radius: var(--border-radius);
    border-top-right-radius: var(--border-radius);
     object-fit: cover;
}

.card-body {
    padding: 1.5rem;
}

.card-title {
    font-size: 1.25rem;
    margin-bottom:.5rem;
}
.card-text {
    color: var(--text-color-dark);
}

/* Custom button styles */
.btn-primary{
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    transition: background-color 0.3s ease;

}
.btn-primary:hover{
     background-color: var(--secondary-color);
    border-color: var(--secondary-color);
}

.btn-primary:focus{
     box-shadow: 0 0 0 .2rem rgba(52,152,219, .5); /* Use secondary color for focus */
}

.btn-outline-primary{
  color: var(--primary-color);
  border-color: var(--primary-color);
    transition: background-color 0.3s;
}

.btn-outline-primary:hover{
    background-color: var(--primary-color);
    color: var(--text-color-light);
}
.btn-secondary
{
      background-color: #6c757d;
        border-color:#6c757d ;
        transition: background-color 0.3s ease
}

.btn-secondary:hover{
    background-color:#545b62;
        border-color:#545b62 ;

}
  .btn-secondary:focus{
             box-shadow: 0 0 0 .2rem rgba(108,117,125, .5); /* match secondary color */
      }



/* Responsive grid adjustments */
.row.row-cols-md-3>.col {
      margin-bottom: 20px;
}
.row.row-cols-1> .col{
      margin-bottom:20px;
}
/* Product detail page layout */
.product-detail {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
}

.product-detail .image-wrapper {
  flex: 1 1 40%; /* Flexible width, starts at 40% */
    max-width: 40%;
    display: flex;
    justify-content: center;
}


.product-detail .product-content{
 flex: 1 1 50%; /* Flexible width, starts at 50% */
 max-width: 50%;

}

 .product-detail .image-wrapper img {
    width: 100%;
    height: auto; /* Keep the natural height */
    max-height: 400px;  /* Limit height if necessary */
     object-fit: cover;

    border-radius: var(--border-radius);

}

/* Image gallery styling */
.image-gallery {

    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
   justify-content: center;
    gap: 10px;
}

.image-gallery img {
    width: 80px;
    height: 80px;
    border-radius:  var(--border-radius);
    object-fit: cover;
     cursor : pointer;
    transition : transform .3 ease;
}

.image-gallery img:hover {
  transform: scale(1.1)
}
/* Filter sidebar styling */

.sidebar {
    padding: 15px;
   background: var(--bg-light);
    box-shadow: var(--box-shadow);
    border-radius: var(--border-radius);
}


.sidebar h3 {
  margin-bottom: 1rem;
      color: var(--primary-color);
}
.sidebar .form-label{
    color: var(--primary-color);
}
.sidebar .form-select,.sidebar .form-control
{

    border-radius: var(--border-radius);
 height: auto;
 box-shadow: none;
  border: 1px solid #ced4da

}


/* Footer customization */
footer {
    background-color: var(--bg-light);
    color: var(--primary-color);
     box-shadow: var(--box-shadow);
}

/* Size and color selectors */
.size-selector,.color-selector {
    margin-bottom: 15px;
}

.size-selector label,.color-selector label
{
  display: block;
    margin-bottom: 0.5rem;
      color: var(--primary-color);
}

.size-selector select,.color-selector select{

    border-radius: var(--border-radius);
     height: auto;
      border: 1px solid #ced4da
}

/* Quantity input styling */
.quantity-selector{
    margin-bottom: 15px;
    display:flex;
    gap:0.5rem;
    align-items:center;
}
.quantity-selector label{
     margin-bottom: 0;
       color: var(--primary-color);
}
.quantity-selector input[type="number"] {
     width: 80px;
     border-radius: var(--border-radius);
    text-align:center;
      border: 1px solid #ced4da
}

/* Review section layout */
.review-section {
    margin-top: 20px;
}
.review-section h2 {
       color: var(--primary-color);
    margin-bottom : 1rem;

}


.review {
    border: 1px solid #ddd;
    padding: 15px;
    margin-bottom: 10px;
        border-radius: var(--border-radius);
        background: var(--bg-light);
}

.review h5 {
    margin-top: 0;
     color: var(--primary-color);
}

.review div {
    color: var(--text-color-dark);
}

/* Responsive Breakpoints */
@media (max-width: 768px) {
    .product-detail {
        flex-direction: column;
    }
       .product-detail .image-wrapper, .product-detail .product-content {
        max-width: 100%;
    }


       .product-detail .image-wrapper img {

    max-height: 300px;
        }
     .row.row-cols-md-3>.col {
      margin-bottom: 10px;
        }

}
C:\mygit\BLazy\repo\nodetest\data\sweaters.js
Language detected: javascript
// filepath: C:\mygit\BLazy\repo\nodetest\data\products.js
const products = [
    {
        id: 1,
        name: 'Classic Cable Knit Sweater',
        price: 79.99,
        description: 'A timeless cable knit sweater, perfect for any occasion.',
        availableSizes: ['S', 'M', 'L', 'XL'],
        availableColors: ['Cream', 'Navy', 'Gray'],
        materialComposition: '100% Cotton',
        careInstructions: 'Machine wash cold, tumble dry low',
         imageUrl: ['/images/cable-knit-1.jpg', '/images/cable-knit-2.jpg'],
         category: 'Pullover',
        reviews: [
            { user: 'Sarah J.', rating: 5, comment: 'Love this sweater! So comfy and warm.' },
            { user: 'Tom B.', rating: 4, comment: 'Great fit and quality.' }
        ],
        stockStatus: 'In Stock'
    },
    {
        id: 2,
        name: 'Striped Merino Wool Sweater',
        price: 99.99,
        description: 'A stylish striped sweater made from soft merino wool.',
        availableSizes: ['XS', 'S', 'M', 'L'],
        availableColors: ['Black/White', 'Navy/Red', 'Green/Gray'],
        materialComposition: '100% Merino Wool',
        careInstructions: 'Hand wash recommended',
          imageUrl: ['/images/merino-striped-1.jpg', '/images/merino-striped-2.jpg'],
        category: 'Pullover',
        reviews: [
            { user: 'Emily L.', rating: 5, comment: 'Super soft and cozy.' },
            { user: 'Chris M.', rating: 4, comment: 'Stylish sweater, perfect for fall.' }
        ],
        stockStatus: 'In Stock'
    },
    {
        id: 3,
        name: 'Oversized Chunky Knit Cardigan',
        price: 119.99,
        description: 'An oversized, chunky knit cardigan, perfect for layering.',
        availableSizes: ['S/M', 'L/XL'],
        availableColors: ['Beige', 'Charcoal', 'Dusty Rose'],
        materialComposition: '50% Acrylic, 50% Wool',
        careInstructions: 'Dry clean only',
         imageUrl: ['/images/chunky-cardigan-1.jpg', '/images/chunky-cardigan-2.jpg'],
        category: 'Cardigan',
         reviews: [
            {user:'Jane D.', rating: 5, comment: 'Love the oversized fit!'},
             {user:'Peter K.', rating: 4, comment:"Great for chilly evenings"}
         ],
        stockStatus: 'Limited Stock'
    },
   {
        id: 4,
        name: 'Cashmere Turtle Neck Sweater',
        price: 149.99,
         description: 'A luxurious cashmere turtleneck, soft and comfortable.',
        availableSizes: ['S', 'M', 'L', 'XL'],
        availableColors: ['Ivory', 'Black', 'Pale Gray'],
        materialComposition: '100% Cashmere',
        careInstructions: 'Hand wash cold',
         imageUrl: ['/images/cashmere-turtleneck-1.jpg', '/images/cashmere-turtleneck-2.jpg'],
        category: 'Turtleneck',
         reviews: [
            {user:'Jessica P.', rating: 5, comment: 'So soft and warm!'},
             {user:'David G', rating: 5, comment: 'Worth every penny'}
         ],
       stockStatus: 'In Stock'
    },
    {
        id: 5,
       name: 'Fleece Zip-Up Sweater',
        price: 69.99,
        description: 'A comfortable fleece zip-up, perfect for casual wear.',
        availableSizes: ['S', 'M', 'L', 'XL', 'XXL'],
        availableColors: ['Navy', 'Green', 'Light Gray'],
         materialComposition: '100% Polyester Fleece',
       careInstructions: 'Machine wash warm, tumble dry low',
          imageUrl:  ['/images/fleece-zip-1.jpg', '/images/fleece-zip-2.jpg'],
        category: 'Zip-up',
         reviews: [
            {user:'Mark W', rating: 4, comment: 'Great for outdoor activities!'},
              {user:'Ashley R', rating: 3, comment: 'Good quality, but could be softer'}
         ],
               stockStatus: 'Low Stock'
    },
    {
        id: 6,
        name: 'Fair Isle Pattern Sweater',
        price: 89.99,
        description: 'A classic Fair Isle style sweater, with a festive pattern.',
        availableSizes: ['XS', 'S', 'M', 'L'],
        availableColors: ['Red/White', 'Blue/Gray', 'Green/Cream'],
        materialComposition: '100% Wool Blend',
         careInstructions: 'Hand wash recommended ',
        imageUrl: ['/images/fair-isle-1.jpg', '/images/fair-isle-2.jpg'],
        category: 'Pullover',
          reviews: [
            {user:'Olivia T', rating: 4, comment:'Beautiful pattern, perfect for the holidays'},
              {user:'Ryan G', rating: 3, comment:'Runs a bit small'}
         ],
          stockStatus: 'In Stock'
    },
    {
        id: 7,
       name: 'Lightweight Cotton V-neck Sweater',
        price: 59.99,
        description:'A lightweight cotton v-neck sweater,ideal for warmer days.',
        availableSizes: ['S', 'M', 'L', 'XL'],
         availableColors: ['Sky Blue', 'Mint Green', 'Coral'],
        materialComposition: '100% Cotton',
        careInstructions: 'Machine wash cool, tumble dry low',
        imageUrl: ['/images/cotton-vneck-1.jpg', '/images/cotton-vneck-2.jpg'],
        category:'Pullover',
         reviews: [
            {user:'Linda C', rating: 5, comment: 'Great for layering'},
              {user:'Steven C', rating: 4, comment: 'Nice color options'}
         ],
                   stockStatus: 'In Stock'
    },
    {
        id: 8,
        name: 'Wool Blend Shawl Collar Cardigan',
         price: 109.99,
        description: 'A warm, wool blend cardigan with a shawl collar.',
        availableSizes: ['S/M', 'L/XL'],
        availableColors: ['Heather Gray', 'Burgundy', 'Forest Green'],
       materialComposition: '70% Wool, 30% Acrylic',
        careInstructions: 'Dry clean only',
         imageUrl: ['/images/shawl-cardigan-1.jpg', '/images/shawl-cardigan-2.jpg'],
        category: 'Cardigan',
           reviews: [
            {user:'Karen L', rating: 5, comment:'Beautiful cardigann!'},
              {user:'Mike J', rating: 4, comment:'Comfortable and stylish'}
         ],
            stockStatus: 'In Stock'
    },
    {
        id: 9,
      name: 'Ribbed Knit Mock Neck Sweater',
       price: 74.99,
        description: 'A versatile ribbed knit mock neck sweater.',
         availableSizes: ['XS', 'S', 'M', 'L'],
        availableColors: ['Black','White','Caramel'],
        materialComposition: '50% Cotton, 50% Polyester',
         careInstructions: 'Machine wash gentle',
        imageUrl: ['/images/mock-neck-1.jpg','/images/mock-neck-2.jpg'],
       category: 'Turtleneck',
           reviews: [
            {user:'Anna B', rating: 4, comment: 'Fits great an goes wit everything'},
              {user:'Robert W', rating: 3, comment: 'A bit thin'}
         ],
           stockStatus: 'Out of Stock'
   },
    {
       id:10,
        name: 'Longline Hooded Cardigan',
         price: 84.99,
       description: 'A fashionable longline hooded cardigan.',
        availableSizes: ['S', 'M', 'L'],
        availableColors: ['Dark Gray', 'Olive Brown', 'Navy'],
       materialComposition: '60% Cotton, 40% Rayon',
        careInstructions: 'Machine wash cold',
        imageUrl: ['/images/hooded-cardigan-1.jpg','/images/hooded-cardigan-2.jpg'],
        category: 'Cardigan',
           reviews: [
            {user:'Rachel S', rating: 5, comment: 'So comfy'},
                {user:'Paul M', rating: 5, comment: 'Nice for everyday '}
         ],
             stockStatus: 'In Stock'
    }

];

module.exports = products;
