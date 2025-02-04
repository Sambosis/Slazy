C:\mygit\BLazy\repo\nodetest\views\layout.ejs
Language detected: html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><%= title %></title>
    
    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="/css/style.css">
</head>
<body>
    <!-- Navigation Bar -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container">
            <a class="navbar-brand" href="/">My App</a>
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
                    <li class="nav-item">
                        <a class="nav-link" href="/cart">Cart</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content Area -->
    <main class="container mt-4">
        <%- body %>
    </main>

    <!-- Footer -->
    <footer class="bg-light text-center text-lg-start mt-4">
        <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
            © 2023 My App
        </div>
    </footer>

    <!-- Bootstrap JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
</body>
</html>
C:\mygit\BLazy\repo\nodetest\views\index.ejs
Language detected: python
import os
from flask import Flask, render_template

app = Flask(__name__)

# Sample product data (replace with your actual data source)
sweaters = [
    {
        "id": 1,
        "name": "Cozy Knit Sweater",
        "price": 49.99,
        "description": "A warm and comfortable sweater for chilly days.",
        "image": "/static/images/sweater1.jpg",
        "alt_text": "Cozy Knit Sweater"
    },
    {
        "id": 2,
        "name": "Stylish V-Neck Sweater",
        "price": 59.99,
        "description": "A fashionable V-neck sweater for a casual look.",
        "image": "/static/images/sweater2.jpg",
        "alt_text": "Stylish V-Neck Sweater"
    },
     {
        "id": 3,
        "name": "Classic Crewneck Sweater",
        "price": 49.99,
        "description": "A timeless crewneck sweater that is good for any occasion.",
        "image": "/static/images/sweater3.jpg",
        "alt_text": "Classic Crewneck Sweater"
    },
    {
        "id": 4,
        "name": "Bold Pattern Sweater",
        "price": 69.99,
        "description": "A bold and bright patterned sweater to show off your unique style.",
        "image": "/static/images/sweater4.jpg",
        "alt_text": "Bold Pattern Sweater"
    }
]

featured_products = [
    {
        "id": 2,
        "name": "Stylish V-Neck Sweater",
         "price": 59.99,
        "description": "A fashionable V-neck sweater for a casual look.",
        "image": "/static/images/sweater2.jpg",
        "alt_text": "Stylish V-Neck Sweater"
        

    },
     {
        "id": 3,
        "name": "Classic Crewneck Sweater",
        "price": 49.99,
        "description": "A timeless crewneck sweater that is good for any occasion.",
        "image": "/static/images/sweater3.jpg",
        "alt_text": "Classic Crewneck Sweater"
    }
]

@app.route('/')
def home():
    return render_template('home.html', sweaters=sweaters, featured_products=featured_products)



if __name__ == '__main__':
    app.run(debug=True)
C:\mygit\BLazy\repo\nodetest\views\cart.ejs
Language detected: python
import os
from flask import Flask, render_template

app = Flask(__name__)

# Sample product data (replace with your actual data source)
sweaters = [
    {
        "id": 1,
        "name": "Cozy Knit Sweater",
        "price": 49.99,
        "description": "A warm and comfortable sweater for chilly days.",
        "image": "/static/images/sweater1.jpg",
         "alt_text": "Cozy Knit Sweater"
    },
    {
        "id": 2,
        "name": "Stylish V-Neck Sweater",
        "price": 59.99,
        "description": "A fashionable V-neck sweater for a casual look.",
        "image": "/static/images/sweater2.jpg",
        "alt_text": "Stylish V-Neck Sweater"
    },
     {
        "id": 3,
        "name": "Classic Crewneck Sweater",
        "price": 49.99,
        "description": "A timeless crewneck sweater that is good for any occasion.",
        "image": "/static/images/sweater3.jpg",
        "alt_text": "Classic Crewneck Sweater"
    },
    {
        "id": 4,
        "name": "Bold Pattern Sweater",
        "price": 69.99,
        "description": "A bold and bright patterned sweater to show off your unique style.",
        "image": "/static/images/sweater4.jpg",
         "alt_text": "Bold Pattern Sweater"
    }
]

featured_products = [
    {
        "id": 2,
        "name": "Stylish V-Neck Sweater",
         "price": 59.99,
        "description": "A fashionable V-neck sweater for a casual look.",
        "image": "/static/images/sweater2.jpg",
        "alt_text": "Stylish V-Neck Sweater"
        

    },
     {
        "id": 3,
        "name": "Classic Crewneck Sweater",
        "price": 49.99,
        "description": "A timeless crewneck sweater that is good for any occasion.",
        "image": "/static/images/sweater3.jpg",
        "alt_text": "Classic Crewneck Sweater"
    }
]

# Sample cart data (replace with your actual cart implementation)
cart_items = [
    {
    "id": 2,
    "name": "Stylish V-Neck Sweater",
    "price": 59.99,
    "image": "/static/images/sweater2.jpg",
    "alt_text": "Stylish V-Neck Sweater",
    "quantity": 2
    },
    {
        "id": 3,
        "name": "Classic Crewneck Sweater",
        "price": 49.99,
        "image": "/static/images/sweater3.jpg",
        "alt_text": "Classic Crewneck Sweater",
        "quantity": 1
    }
]

@app.route('/')
def home():
    return render_template('home.html', sweaters=sweaters, featured_products=featured_products)

@app.route('/cart')
def cart():
    return render_template('cart.html', cart_items=cart_items)


if __name__ == '__main__':
    app.run(debug=True)
C:\mygit\BLazy\repo\nodetest\public\css\style.css
Language detected: python
import os
from flask import Flask, render_template

app = Flask(__name__)

# Sample product data (replace with your actual data source)
sweaters = [
    {
        "id": 1,
        "name": "Cozy Knit Sweater",
        "price": 49.99,
        "description": "A warm and comfortable sweater for chilly days.",
        "image": "/static/images/sweater1.jpg",
        "alt_text": "Cozy Knit Sweater"
    },
    {
        "id": 2,
        "name": "Stylish V-Neck Sweater",
        "price": 59.99,
        "description": "A fashionable V-neck sweater for a casual look.",
        "image": "/static/images/sweater2.jpg",
        "alt_text": "Stylish V-Neck Sweater"
    },
     {
        "id": 3,
        "name": "Classic Crewneck Sweater",
        "price": 49.99,
        "description": "A timeless crewneck sweater that is good for any occasion.",
        "image": "/static/images/sweater3.jpg",
        "alt_text": "Classic Crewneck Sweater"
    },
    {
        "id": 4,
        "name": "Bold Pattern Sweater",
        "price": 69.99,
        "description": "A bold and bright patterned sweater to show off your unique style.",
        "image": "/static/images/sweater4.jpg",
        "alt_text": "Bold Pattern Sweater"
    }
]

featured_products = [
    {
        "id": 2,
        "name": "Stylish V-Neck Sweater",
         "price": 59.99,
        "description": "A fashionable V-neck sweater for a casual look.",
        "image": "/static/images/sweater2.jpg",
        "alt_text": "Stylish V-Neck Sweater"
        

    },
     {
        "id": 3,
        "name": "Classic Crewneck Sweater",
        "price": 49.99,
        "description": "A timeless crewneck sweater that is good for any occasion.",
        "image": "/static/images/sweater3.jpg",
        "alt_text": "Classic Crewneck Sweater"
    }
]

# Sample cart data (replace with your actual cart implementation)
cart_items = [
    {
    "id": 2,
    "name": "Stylish V-Neck Sweater",
    "price": 59.99,
    "image": "/static/images/sweater2.jpg",
    "alt_text": "Stylish V-Neck Sweater",
    "quantity": 2
    },
    {
        "id": 3,
        "name": "Classic Crewneck Sweater",
        "price": 49.99,
        "image": "/static/images/sweater3.jpg",
        "alt_text": "Classic Crewneck Sweater",
        "quantity": 1
    }
]


@app.route('/')
def home():
    return render_template('home.html', sweaters=sweaters, featured_products=featured_products)

@app.route('/cart')
def cart():
    return render_template('cart.html', cart_items=cart_items)


if __name__ == '__main__':
    app.run(debug=True)
