# Shop Project

This is a Django-based e-commerce application that allows users to browse products, add them to a shopping cart, and place orders. The project includes features such as product categorization, order management, and a simple payment API.

## Features

- **Product Management**: Add, update, and delete products.
- **Category Management**: Organize products into categories and subcategories.
- **Shopping Cart**: Add products to the cart, update quantities, and remove items.
- **Order Management**: Place orders, view order details, and manage order status.
- **Admin Interface**: Manage products, categories, and orders through the Django admin panel.
- **API Integration**: Integrate with external APIs for payment processing and other functionalities.
- **Celery Integration**: Asynchronous task processing using Celery.
- **Payment API**: A simple API endpoint for marking orders as paid.

## Installation

### Requirements (for local installation)
- Python 3.x
- PostgreSQL
- Redis
- RabbitMQ

If using Docker, these dependencies are included in the container setup.

### Steps

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/shop.git
    cd shop
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up the database**:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Load initial data** (if applicable):
    ```sh
    python manage.py loaddata dump.json
    ```

6. **Run the development server**:
    ```sh
    python manage.py runserver
    ```

## Docker Setup

1. **Build and run the Docker containers**:
    ```sh
    docker network create shared_network
    ```

2. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

3. **Access the application**:
    - Web application: `http://localhost:8001`
    - Admin interface: `http://localhost:8001/admin`

## Environment Variables

Create a `.env` file in the project root and add the following environment variables:

```env
POSTGRES_DB=shop
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
CLIENT_ID=your_client_id
CLIENT_SECRET=your_client_secret
ACCESS_TOKEN_URL=your_access_token_url
```

## API Endpoints

### Payment API

#### Mark an Order as Paid
- **Endpoint**: `POST /api/paid/`
- **Request Body**:
    ```json
    {
      "order_id": 1,
      "is_paid": true
    }
    ```
- **Responses**:
  - `200 OK`: Payment successful, returns a redirect link.
  - `400 Bad Request`: Order is already paid or invalid request.
  - `404 Not Found`: Order does not exist.

## Usage

- **Admin Interface**: Access the admin panel at `/admin` to manage products, categories, and orders.
- **Shopping Cart**: Browse products, add them to the cart, and proceed to checkout.
- **Order Management**: View order details and manage order status.


## License

This project is licensed under the [MIT License](LICENSE.txt).

