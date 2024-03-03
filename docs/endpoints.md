# API Endpoints Documentation

This document provides detailed information about the API endpoints available in the application, including how to use them and example requests and responses.

## Endpoints Overview

## Testing with Authentication in DRF_yasg

All endpoints requiring authentication can be tested in DRF_yasg after obtaining an access token. Follow these steps to authorize:

1. Obtain your token via the login endpoint (`api/v1/api-token-auth/`).
2. In the DRF_yasg UI, locate the "Authorize" button in the TokenAuth (apiKey) section.
3. In the input field, enter your token in the following format: `Token <token_from_login_endpoint>`
4. Click "Authorize" to apply the token for subsequent requests.

This will enable you to test all authenticated endpoints within the DRF_yasg interface.


### Authentication

#### Login

To authenticate and receive an access token, send a POST request to the login endpoint. This token is required for accessing protected endpoints.

**Endpoint:** `api/v1/api-token-auth/`

**Method:** `POST`

**Request Body:**

```json
{
  "username": "string",
  "password": "string"
}
```

### Creating a Product

To add a new product to the system, send a POST request to the product creation endpoint. This operation requires authentication, so make sure to include your access token obtained from the login endpoint.

**Endpoint:** `api/v1/products/`

**Method:** `POST`

**Authorization:** Authorization Token (Obtained from login)

**Request Body:**

```json
{
  "name": "string",
  "initial_price": "number"
}
```

### Adding or Updating Product Prices

To add or update the price of a product, send a POST request to the prices endpoint. This operation requires authentication.

**Endpoint:** `/api/v1/prices/`

**Method:** `POST`

**Authorization:** Authorization Token (Obtained from login)

**Content-Type:** `application/json`

**Request Body:**

```json
{
  "product": {product_id},
  "price": number,
  "start_date": "YYYY-MM-DD",
  "end_date": "YYYY-MM-DD"
}
```


### Getting the Average Price of a Product

To retrieve the average price of a product over a specified time period, send a GET request to the average price endpoint. This operation require authentication

**Endpoint:** `/api/v1/prices/{product_id}/average_price/`

**Method:** `GET`

**Authorization:** Authorization Token (Obtained from login)

**URL Parameters:**

- `{product_id}`: The unique identifier of the product for which the average price is being requested.

**Query Parameters:** (Optional)

You can optionally include `from_date` and `to_date` query parameters in the request URL to specify the time period for which the average price should be calculated. If these parameters are not provided, the system might default to calculating the average price over all available data.

### Retrieving Detailed Product Information

To get detailed information about a product, over a specified period, send a GET request to the detailed information endpoint. This operation require authentication.

**Endpoint:** `/api/v1/products/{product_id}/detailed_info/`

**Method:** `GET`

**Authorization:** Authorization Token (Obtained from login)

**URL Parameters:**

- `product_id`: The unique identifier of the product for which detailed information is being requested.

**Response:**

A successful request will return a JSON object containing detailed information about the product

**Example Response:**

```json
{
    "product_name": "p1",
    "current_price": 200.0,
    "price_history": [
        {
            "start_date": "2024-02-27",
            "end_date": null,
            "price": 20.0
        },
        {
            "start_date": "2024-02-28",
            "end_date": null,
            "price": 40.0
        },
    ]
}
```
