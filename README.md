# Order Processing System Documentation

## Introduction
This documentation provides instructions on setting up and running the Order Processing System, a simplified solution for managing orders in an online store. The system handles various aspects of order processing, including stock management, payment processing, sending order confirmation emails, and error handling.

## Required Feature
-**Stock Management** Implement functionality to validate the availability of products in the store's inventory when placing an order. Ensure that the system updates the stock count accordingly after each successful order.

-**Payment Processing: Integrate with a mock payment gateway to simulate payment processing. Upon successful payment, mark the order as paid and proceed with order fulfillment.

-**Order Confirmation Emails** Sending order confirmation emails to customers after a successful purchase. The email has details the order ID, order date, purchased items (name, price, quantity, total price), and total amount of the order.

-**Error Handling** Managing any issues that may occur during the order processing flow, such as stock unavailability or payment failures.

- **Containerization**: Creating a Dockerfile to package the application into a container.

- **Repository Integration**: Push the built Docker image to (Docker Hub) you will see DockerHub link in end of file.

## Additional Features
- **User Authentication:** Basic user authentication is implemented to ensure only registered users can place order (JWT).
- **Customization:** Email templates for order confirmation emails can be customized. (by making Html file for email)

## Setup

### Docker Setup
To run the Order Processing System using Docker, follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd order-processing-system
   ```

2. Build the Docker image:
   ```bash
   docker build -t order-processing-system .
   ```

3. Run the Docker container:
   ```bash
   docker run -p 8000:8000 order-processing-system
   ```

### Virtual Environment Setup
If you prefer not to use Docker, you can set up the project using a virtual environment. Follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd order-processing-system
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # for Linux/macOS
   # or
   venv\Scripts\activate  # for Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install djangorestframework_simplejwt
   ```

4. Run the Django server:
   ```bash
   python manage.py runserver
   ```

## Dependencies
The Order Processing System relies on the following dependencies:
- Django: Web framework for building the application.
- Django REST Framework (DRF): Toolkit for building Web APIs.
- Requests: HTTP library for making requests to external services.
- Django REST Framework SimpleJWT: Library for JWT authentication.

## Endpoints
### Postman Documentation
For detailed documentation and testing of the endpoints, refer to the [Postman documentation](https://www.postman.com/winter-meteor-327606/workspace/appgain-backendtask/collection/31151980-17fc9f0b-5c38-46d6-ab25-2a0e2cbe5893?action=share&creator=31151980).
note that it may not be opened in Microsoft Edge. open it in Chrome.

## admin App:

### you can open admin page by email:hesham@gmail.com , password: hesham2002

### accounts App:

#### 1. `/register/`

- **Method:** POST
- **Description:** Register a new user.
- **Notes:**
  - Requires providing email, username, and password in the request body.
- **Example:**
  ```http
  POST /register/
  ```
  **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "username": "example_user",
    "password": "password123"
  }
  ```
  **Response:**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "example_user",
    "phone_number": null
  }
  ```

#### 2. `/login/`

- **Method:** POST
- **Description:** Log in with existing user credentials and obtain authentication tokens.
- **Notes:**
  - Requires providing email and password in the request body.
- **Example:**
  ```http
  POST /login/
  ```
  **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "password123"
  }
  ```
  **Response:**
  ```json
  {
    "refresh": "refresh_token",
    "access": "access_token"
  }
  ```

#### 3. `/token/refresh/`

- **Method:** POST
- **Description:** Refresh the access token using the refresh token.
- **Notes:**
  - Requires providing the refresh token in the request body.
- **Example:**
  ```http
  POST /token/refresh/
  ```
  **Request Body:**
  ```json
  {
    "refresh": "refresh_token"
  }
  ```
  **Response:**
  ```json
  {
    "access": "new_access_token"
  }
  ```

#### 4. `/user/`

- **Method:** GET
- **Description:** Retrieve details of the authenticated user.
- **Notes:**
  - Requires authentication using the access token.
  - Returns details of the currently authenticated user.
- **Example:**
  ```http
  GET /user/
  ```
  **Response:**
  ```json
  {
    "id": 1,
    "email": "user@example.com",
    "username": "example_user",
    "phone_number": null
  }
  ```

Regarding setting up authentication in Postman, follow these steps:

1. Open Postman and create a new request.
2. Choose the appropriate HTTP method (e.g., POST for login/register endpoints).
3. Enter the endpoint URL (e.g., `http://localhost:8000/login/`).
4. Navigate to the "Headers" tab and add a new header with key `Content-Type` and value `application/json`.
5. In the "Body" tab, select "raw" and choose JSON format.
6. Enter the necessary request body parameters (e.g., email and password for login).
7. Send the request to receive authentication tokens (access and refresh tokens).
8. For subsequent requests that require authentication, add the access token to the request headers:
   - Create a new header with key `Authorization` and value `Bearer <access_token>`.

### Store App:

#### 1. `/products/`

- **Method:** GET
- **Description:** Retrieve a list of all products.
- **Notes:**
  - Requires authentication.
  - Only authenticated users can access this endpoint.
- **Example:**
  ```http
  GET /products/
  ```
  **Response:**
  ```json
  [
    {
      "id": 1,
      "name": "Product A",
      "description": "Description of Product A",
      "price": 50.00,
      "stock": 100
    },
    {
      "id": 2,
      "name": "Product B",
      "description": "Description of Product B",
      "price": 30.00,
      "stock": 50
    }
  ]
  ```

#### 2. `/place_order/`

- **Method:** POST
- **Description:** Place a new order.
- **Notes:**
  - Requires authentication.
  - Only authenticated users can access this endpoint.
  - Requires providing a list of items in the request body.
- **Example:**
  ```http
  POST /place_order/
  ```
  **Request Body:**
  ```json
  {
    "items": [
      {"productName": "Product A", "quantity": 2},
      {"productName": "Product B", "quantity": 1}
    ]
  }
  ```
  **Response:**
  ```json
  {
    "id": 1,
    "customer": "username",
    "total_amount": 130.00,
    "paid": false,
    "created_at": "2024-05-04T12:00:00Z"
  }
  ```

#### 3. `/orders/`

- **Method:** GET
- **Description:** Retrieve a list of orders placed by the authenticated user.
- **Notes:**
  - Requires authentication.
  - Only authenticated users can access this endpoint.
- **Example:**
  ```http
  GET /orders/
  ```
  **Response:**
  ```json
  [
    {
      "id": 1,
      "customer": "username",
      "total_amount": 130.00,
      "paid": false,
      "created_at": "2024-05-04T12:00:00Z"
    }
  ]
  ```

#### 4. `/make_payment/`

- **Method:** POST
- **Description:** Process payment for an order.
- **Notes:**
  - Requires authentication.
  - Only authenticated users can access this endpoint.
  - Requires providing order ID in the request body.
- **Example:**
  ```http
  POST /make_payment/
  ```
  **Request Body:**
  ```json
  {
    "order_id": 1,
    "amount": 130.00,
    "card_number": "1234567890123456",
    "expiry_date": "12/24",
    "cvv": "123"
  }
  ```
  **Response:**
  ```json
  {
    "message": "Payment successful",
    "order_data": {
      "order_id": 1,
      "total_amount": 130.00,
      "created_at": "2024-05-04T12:00:00Z",
      "items": [
        {
          "product": "Product A",
          "price": 50.00,
          "quantity": 2,
          "totalprice": 100.00
        },
        {
          "product": "Product B",
          "price": 30.00,
          "quantity": 1,
          "totalprice": 30.00
        }
      ]
    }
  }
  ```

#### 5. `/orders/`

- **Method:** GET
- **Description:** Retrieve a list of orders belonging to the authenticated user.
- **Notes:**
  - Requires authentication.
  - Only authenticated users can access this endpoint.
  - Returns orders filtered by the authenticated user.
- **Example:**
  ```http
  GET /orders/
  ```
  **Response:**
  ```json
  [
    {
      "id": 1,
      "customer": "username",
      "total_amount": 130.00,
      "paid": false,
      "created_at": "2024-05-04T12:00:00Z"
    }
  ]
  ```

![Postman image](Postman.jpg)

## Docker Hub
This is the Docker Hub repository containing the latest Docker image of the Order Processing System.
[Docker Hub Submission](https://hub.docker.com/layers/heshamabedelatty/orderprocessingsystem/latest/images/sha256:eb6c8e565458978e28e175ba9a8b1f4a0ed519b2b416e87eb97b186a02ede107?uuid=6FE18E5C-6512-470D-8941-547B5CDC0CEE)




