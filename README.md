# Introduction
Product Price Tracker is a Django application designed to monitor and analyze the fluctuating prices of products in the market. Users can add products, update their prices for any period, including indefinite future pricing, and modify past prices as needed. The application calculates and displays the average price of a product for a specified period, providing valuable insights into market trends and aiding in strategic decision-making.

## Installation

Choose the installation method that best fits your needs:

- [System Installation](./docs/system_installation.md)
- [Docker Installation](./docs/docker_installation.md)

### Creating a Django Superuser
Depending on your installation method, the process to create a superuser will slightly vary:

If you installed the application directly on your system, ensure your virtual environment is activated, then navigate to your project directory and run the following command:
```
python manage.py createsuperuser
```

If you are using Docker Compose

```
docker-compose exec app python manage.py createsuperuser
```

## Testing Endpoints with Swagger UI
The Market Price Tracker incorporates the `drf_yasg` package, providing a Swagger UI interface for an interactive exploration of the API's endpoints. This feature enables users to test the application's functionalities directly from their browser, making it easier to understand and utilize the API's capabilities.

Accessing Swagger UI
After setting up the application (via either system installation or Docker), the Swagger UI can be accessed at:

URL: http://localhost:8000/doc/

This interface provides a comprehensive overview of all available endpoints, allowing you to execute API requests and receive responses within the UI.


## Available Endpoints
A variety of endpoints are available for testing different functionalities of the Market Price Tracker, including adding products, updating prices, and fetching average prices. For a detailed description of most important endpoints, including request parameters and response formats, please refer to:

- [Endpoints Documentation](./docs/endpoints.md)