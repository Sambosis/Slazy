C:\mygit\BLazy\repo\nodetest\app.js
Language detected: javascript
const express = require('express');
const bodyParser = require('body-parser');
const morgan = require('morgan');
const path = require('path');

const app = express();
const port = 3000;

// Configure middleware
app.use(morgan('dev'));
app.use(bodyParser.urlencoded({ extended: false }));
app.use(express.static(path.join(__dirname, 'public')));


// Set EJS as the view engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Basic data structure for sweaters
const sweaters = [
  { id: 1, name: 'Classic Wool Sweater', price: 75, description: 'A warm and cozy wool sweater.', imageUrl: '/images/sweater1.jpg'},
  { id: 2, name: 'Cotton Crewneck', price: 50, description: 'Lightweight everyday crewneck.', imageUrl: '/images/sweater2.jpg' },
  { id: 3, name: 'Cashmere V-Neck', price: 150, description: 'Luxurious cashmere V-neck sweater.', imageUrl:'/images/sweater3.jpg' }
];

// Routes
app.get('/', (req, res) => {
  res.render('index', { sweaters });
});

app.get('/sweater/:id', (req, res) => {
  const sweaterId = parseInt(req.params.id);
  const sweater = sweaters.find(s => s.id === sweaterId);
  if(sweater) {
     res.render('sweater', { sweater })
  } else {
    res.status(404).send('Sweater not found');
  }
});

app.get('/about', (req, res) => {
  res.render('about');
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send('Something broke!');
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
C:\mygit\BLazy\repo\nodetest\views\layout.ejs
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sweater Store</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    <link rel="stylesheet" href="/css/style.css">
    
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
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
                <a class="nav-link" href="/about">About</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

    <div class="container mt-4">
        <%- body %>
    </div>

    <footer class="mt-5 py-3 bg-light text-center">
        <p>&copy; 2024 Sweater Store. All rights reserved.</p>
        <p>123 Main Street, Anytown, USA </p>
    </footer>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    
</body>
</html>
C:\mygit\BLazy\repo\nodetest\views\index.ejs
Language detected: ejs
<%- include('layout', {body: ''}); %>

<div class="p-5 mb-4 bg-light rounded-3">
    <div class="container py-5">
      <h1 class="display-5 fw-bold">Welcome to Our Sweater Store</h1>
      <p class="col-md-8 fs-4">Find the perfect cozy sweater for any occasion. Browse our collection below!</p>
    </div>
  </div>
  
  <div class="row row-cols-1 row-cols-md-3 g-4">
    <% sweaters.forEach(sweater => { %>
      <div class="col">
        <div class="card h-100">
          <img src="<%= sweater.imageUrl %>" class="card-img-top" alt="<%= sweater.name %>">
          <div class="card-body">
            <h5 class="card-title"><%= sweater.name %></h5>
            <p class="card-text">$<%= sweater.price %></p>
            <p class="card-text"><%= sweater.description %></p>
            <a href="/sweater/<%= sweater.id %>" class="btn btn-primary">View Details</a>
          </div>
        </div>
      </div>
    <% }); %>
  </div>
C:\mygit\BLazy\repo\nodetest\public\css\style.css
Language detected: css
/* filepath: C:\mygit\BLazy\repo\nodetest\public\css\style.css */

/*  
    Custom Styles for the Sweater Store 
    Includes:
        - Custom Colors and Branding
        - Card Hover Effects
        - Hero Section Styling
        - Custom Spacing and Padding
        - Responsive Image Handling
        - Footer Styling
        - Navigation Bar Customization
*/


/* -- Color Palette -- */
:root {
    --primary-color: #3498db; /* Blue */
    --secondary-color: #2ecc71; /* Green */
    --light-bg: #f8f9fa;
    --dark-text: #333;
    --light-text: #fff;
    --card-shadow: rgba(0, 0, 0, 0.1);
    --hover-shadow:  rgba(0, 0, 0, 0.2);
}

/* -- General Styles -- */
body {
    font-family: 'Arial', sans-serif;
    color: var(--dark-text);
}

/* -- Navigation Bar Customization -- */
.navbar {
    background-color: var(--light-bg);
    padding: 1rem 0;
    box-shadow: 0 2px 4px var(--card-shadow); /* Add a subtle shadow */
}

.navbar-brand {
    font-weight: bold;
    color: var(--primary-color);
}

.nav-link {
    color: var(--dark-text);
    transition: color 0.3s ease;
  }
  
.nav-link:hover {
    color: var(--primary-color);
    
}
  
.ms-auto {
    margin-left: auto;
}

/* -- Hero Section Styling -- */
.p-5.mb-4.bg-light.rounded-3 {
    background-color: var(--light-bg) !important;
    padding: 3rem !important;
    margin-bottom: 2.5rem !important;
    border-radius: 0.5rem !important;

}
  
.display-5 {
    color: var(--dark-text);
    font-weight: bold;
    margin-bottom: 1rem;
}
  
.fs-4 {
    color: #666;
}  

/* --- Card Styling --- */
.card {
    border: none;
    border-radius: 0.5rem;
    box-shadow: 0 4px 8px var(--card-shadow);    
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 12px var(--hover-shadow);
}
  
.card-img-top {
    height: 200px;
    object-fit: cover;
    border-top-left-radius: 0.5rem;
    border-top-right-radius: 0.5rem;
}

.card-body {
    padding: 1.5rem;
}
  
.card-title {
    font-size: 1.25rem;
    font-weight: bold;
    color: var(--dark-text);
}
  
.card-text {
    color: #555;
    margin-bottom: 0.75rem;
}
  
.btn-primary {
    background-color: var(--primary-color);
    border-color: var(--primary-color);
    transition: background-color 0.3s ease, border-color 0.3s ease;
}
  
.btn-primary:hover {
    background-color: var(--secondary-color);
     border-color: var(--secondary-color);
}

/* -- Custom Spacing and Padding -- */
.container {
    padding-top: 20px;
}
  
.mt-4 {
    margin-top: 40px;
}

/* -- Responsive Image Handling -- */
.card-img-top {
    max-width: 100%;
    height: auto;
  }

/* -- Footer Styling -- */
footer {
    background-color: var(--light-bg);
    color: #777;
    text-align: center;
  }

footer p {
    margin: 0.3rem 0;
    
}
