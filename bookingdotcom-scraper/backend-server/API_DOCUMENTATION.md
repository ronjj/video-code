# Booking.com Hotel Search API Documentation

## Overview

This Flask API provides programmatic access to hotel search functionality, scraping data from Booking.com. The API allows you to search for hotels with various filters and returns structured JSON data.

## Base URL

```
http://localhost:5000
```

## Authentication

No authentication required for this local API.

---

## Endpoints

### 1. Home / Documentation

**GET** `/`

Returns basic API information and available endpoints.

**Response:**

```json
{
  "message": "Booking.com Hotel Search API",
  "version": "1.0.0",
  "endpoints": {
    "/": "This documentation",
    "/search": "Search for hotels",
    "/health": "Health check"
  },
  "documentation": "See /docs for detailed API documentation"
}
```

### 2. Health Check

**GET** `/health`

Returns the health status of the API.

**Response:**

```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00.000Z"
}
```

### 3. Hotel Search

**GET/POST** `/search`

Searches for hotels based on the provided criteria.

#### Required Parameters

- `checkin_date` (string): Check-in date in YYYY-MM-DD format
- `checkout_date` (string): Check-out date in YYYY-MM-DD format

#### Optional Parameters

- `location` (string): Search location (default: "Seattle, United States")
- `dest_id` (integer): Booking.com destination ID (default: 20144883 for Seattle)
- `max_price` (float): Maximum price per night in USD
- `min_stars` (integer): Minimum star rating (1-5)
- `min_reviews` (integer): Minimum number of reviews
- `adults` (integer): Number of adults (default: 2)
- `rooms` (integer): Number of rooms (default: 1)
- `children` (integer): Number of children (default: 0)

#### Example Request (GET)

```
GET /search?checkin_date=2024-07-01&checkout_date=2024-07-05&max_price=200&min_stars=4&min_reviews=50
```

#### Example Request (POST)

```bash
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "checkin_date": "2024-07-01",
    "checkout_date": "2024-07-05",
    "location": "New York, United States",
    "max_price": 300,
    "min_stars": 4,
    "min_reviews": 100,
    "adults": 2,
    "rooms": 1,
    "children": 0
  }'
```

#### Response Structure

```json
{
  "success": true,
  "search_params": {
    "checkin_date": "2024-07-01",
    "checkout_date": "2024-07-05",
    "location": "Seattle, United States",
    "adults": 2,
    "rooms": 1,
    "children": 0,
    "filters": {
      "max_price": 200,
      "min_stars": 4,
      "min_reviews": 50
    }
  },
  "results_count": 25,
  "hotels": [
    {
      "id": "12345",
      "name": "Grand Hotel Seattle",
      "location": {
        "address": "123 Main St",
        "city": "Seattle",
        "full_address": "123 Main St, Seattle"
      },
      "star_rating": 4,
      "guest_rating": {
        "score": 8.5,
        "review_count": 1250,
        "text": "Very good"
      },
      "pricing": {
        "total_price": "US$800",
        "currency": "USD",
        "price_per_night": "US$200",
        "price_per_night_unformatted": 200
      },
      "meal_plan": "Breakfast included",
      "image_url": "https://www.booking.com/hotel/image.jpg"
    }
  ]
}
```

---

## Error Responses

### 400 Bad Request

**Missing Required Parameters:**

```json
{
  "error": "Missing required parameters",
  "message": "checkin_date and checkout_date are required"
}
```

**Invalid Date Format:**

```json
{
  "error": "Invalid date format",
  "message": "Date must be in YYYY-MM-DD format"
}
```

**Invalid Date Logic:**

```json
{
  "error": "Invalid dates",
  "message": "Check-out date must be after check-in date"
}
```

### 500 Internal Server Error

**Search Failed:**

```json
{
  "error": "Search failed",
  "message": "API request failed with status 403"
}
```

---

## Usage Examples

### Python with requests

```python
import requests

# Basic search
response = requests.get('http://localhost:5000/search', params={
    'checkin_date': '2024-07-01',
    'checkout_date': '2024-07-05'
})

hotels = response.json()['hotels']
print(f"Found {len(hotels)} hotels")

# Advanced search with filters
response = requests.post('http://localhost:5000/search', json={
    'checkin_date': '2024-07-01',
    'checkout_date': '2024-07-05',
    'location': 'Paris, France',
    'max_price': 250,
    'min_stars': 4,
    'min_reviews': 100,
    'adults': 2,
    'rooms': 1
})

data = response.json()
if data['success']:
    for hotel in data['hotels']:
        print(f"{hotel['name']} - {hotel['pricing']['price_per_night']}")
```

### JavaScript with fetch

```javascript
// Basic search
fetch(
  "http://localhost:5000/search?" +
    new URLSearchParams({
      checkin_date: "2024-07-01",
      checkout_date: "2024-07-05",
      max_price: "200",
    })
)
  .then((response) => response.json())
  .then((data) => {
    console.log(`Found ${data.results_count} hotels`);
    data.hotels.forEach((hotel) => {
      console.log(`${hotel.name} - ${hotel.pricing.price_per_night}`);
    });
  });

// POST request
fetch("http://localhost:5000/search", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    checkin_date: "2024-07-01",
    checkout_date: "2024-07-05",
    location: "London, United Kingdom",
    min_stars: 4,
  }),
})
  .then((response) => response.json())
  .then((data) => console.log(data));
```

### curl

```bash
# GET request
curl "http://localhost:5000/search?checkin_date=2024-07-01&checkout_date=2024-07-05&max_price=200"

# POST request
curl -X POST http://localhost:5000/search \
  -H "Content-Type: application/json" \
  -d '{
    "checkin_date": "2024-07-01",
    "checkout_date": "2024-07-05",
    "max_price": 200,
    "min_stars": 4
  }'
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Server

```bash
python app.py
```

The server will start on `http://localhost:5000`

### 3. Test the API

```bash
curl http://localhost:5000/health
```

---

## Rate Limiting & Best Practices

1. **Rate Limiting**: Be mindful of making too many requests to avoid being blocked by Booking.com
2. **Caching**: Consider implementing caching for repeated searches
3. **Error Handling**: Always check the `success` field in responses
4. **Date Format**: Always use YYYY-MM-DD format for dates
5. **Validation**: The API validates dates to ensure check-out is after check-in and dates are not in the past

---

## Common Destination IDs

Here are some common destination IDs for major cities:

- Seattle: 20144883
- New York: 20088325
- London: -2601889
- Paris: -1456928
- Tokyo: -246227
- Sydney: -1603135

To find destination IDs for other cities, you can inspect network requests on Booking.com or use their autocomplete API.

---

## Troubleshooting

### Common Issues

1. **403 Forbidden**: The API might be blocked. Try changing user agent or implementing proxy rotation.
2. **Empty Results**: Check if the location and dates are valid.
3. **Timeout**: Increase request timeout or implement retry logic.
4. **Rate Limited**: Add delays between requests.

### Contact

For issues or questions about this API, please check the source code or create an issue in the repository.
