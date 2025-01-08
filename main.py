from fastapi import FastAPI, HTTPException
import requests
import time

app = FastAPI()

# Metrics storage
metrics = {
    'weather/monthly-profile': {'hits': 0, 'errors': 0, 'avg_time': 0.0, 'max_time': 0.0, 'min_time': float('inf')},
    'travel/best-month': {'hits': 0, 'errors': 0, 'avg_time': 0.0, 'max_time': 0.0, 'min_time': float('inf')},
    'travel/compare-cities': {'hits': 0, 'errors': 0, 'avg_time': 0.0, 'max_time': 0.0, 'min_time': float('inf')},
}

def update_metrics(route, start_time, error=False):
    duration = time.time() - start_time
    metrics[route]['hits'] += 1
    if error:
        metrics[route]['errors'] += 1
    metrics[route]['avg_time'] = ((metrics[route]['avg_time'] * (metrics[route]['hits'] - 1)) + duration) / metrics[route]['hits']
    metrics[route]['max_time'] = max(metrics[route]['max_time'], duration)
    metrics[route]['min_time'] = min(metrics[route]['min_time'], duration)

@app.get("/weather/monthly-profile")
def monthly_weather_profile(city: str, month: int):
    start_time = time.time()
    try:
        # Validate month
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="Invalid month. Must be between 1 and 12.")

        # Fetch weather data
        response = requests.get(
            f"https://archive-api.open-meteo.com/v1/archive?latitude=51.5074&longitude=-0.1278&start_date=2018-{month:02d}-01&end_date=2023-{month:02d}-28&daily=temperature_2m_min,temperature_2m_max&timezone=Europe/London"
        )
        response.raise_for_status()
        weather_data = response.json()

        # Extract data and handle missing values
        min_temp_data = [t for t in weather_data['daily']['temperature_2m_min'] if t is not None]
        max_temp_data = [t for t in weather_data['daily']['temperature_2m_max'] if t is not None]

        # Calculate averages
        min_temp_avg = sum(min_temp_data) / len(min_temp_data) if min_temp_data else None
        max_temp_avg = sum(max_temp_data) / len(max_temp_data) if max_temp_data else None

        update_metrics('weather/monthly-profile', start_time)
        return {
            "city": city,
            "month": month,
            "min_temp_avg": round(min_temp_avg, 2) if min_temp_avg else None,
            "max_temp_avg": round(max_temp_avg, 2) if max_temp_avg else None
        }
    except requests.exceptions.RequestException as e:
        update_metrics('weather/monthly-profile', start_time, error=True)
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        update_metrics('weather/monthly-profile', start_time, error=True)
        raise HTTPException(status_code=500, detail=f"Error processing weather data: {str(e)}")

@app.get("/travel/best-month")
def best_travel_month(city: str, min_temp: float, max_temp: float):
    start_time = time.time()
    try:
        # Dummy implementation (replace with actual logic)
        best_month = 6
        min_temp_diff = abs(min_temp - 15)
        max_temp_diff = abs(max_temp - 25)
        overall_diff = min_temp_diff + max_temp_diff

        update_metrics('travel/best-month', start_time)
        return {
            "city": city,
            "best_month": best_month,
            "min_temp_diff": round(min_temp_diff, 2),
            "max_temp_diff": round(max_temp_diff, 2),
            "overall_diff": round(overall_diff, 2)
        }
    except Exception as e:
        update_metrics('travel/best-month', start_time, error=True)
        raise HTTPException(status_code=500, detail=f"Error processing best travel month: {str(e)}")

@app.get("/travel/compare-cities")
def compare_cities(cities: str, month: int):
    start_time = time.time()
    try:
        # Validate month
        if month < 1 or month > 12:
            raise HTTPException(status_code=400, detail="Invalid month. Must be between 1 and 12.")

        city_list = cities.split(',')

        # Prepare response structure
        city_weather_data = {}

        # Fetch weather data for each city
        for city in city_list:
            city_weather_data[city] = {}

            # Replace with actual latitude and longitude for each city
            if city == "New York":
                lat, lon = 40.7128, -74.0060
            elif city == "Tokyo":
                lat, lon = 35.6762, 139.6503
            elif city == "Sydney":
                lat, lon = -33.8688, 151.2093
            else:
                raise HTTPException(status_code=400, detail=f"Weather data for {city} is not available.")

            # Fetch weather data for the city and month
            response = requests.get(
                f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date=2018-{month:02d}-01&end_date=2023-{month:02d}-28&daily=temperature_2m_min,temperature_2m_max&timezone=Europe/London"
            )
            response.raise_for_status()
            weather_data = response.json()

            # Extract data and handle missing values
            min_temp_data = [t for t in weather_data['daily']['temperature_2m_min'] if t is not None]
            max_temp_data = [t for t in weather_data['daily']['temperature_2m_max'] if t is not None]

            # Calculate averages
            min_temp_avg = sum(min_temp_data) / len(min_temp_data) if min_temp_data else None
            max_temp_avg = sum(max_temp_data) / len(max_temp_data) if max_temp_data else None

            # Store the calculated data in the response, ensure no invalid values are returned
            if min_temp_avg is not None:
                city_weather_data[city]["min_temp_avg"] = round(min_temp_avg, 2)
            if max_temp_avg is not None:
                city_weather_data[city]["max_temp_avg"] = round(max_temp_avg, 2)

        update_metrics('travel/compare-cities', start_time)
        return {"month": month, **city_weather_data}

    except requests.exceptions.RequestException as e:
        update_metrics('travel/compare-cities', start_time, error=True)
        raise HTTPException(status_code=500, detail=f"Request error: {str(e)}")
    except Exception as e:
        update_metrics('travel/compare-cities', start_time, error=True)
        raise HTTPException(status_code=500, detail=f"Error comparing cities: {str(e)}")



@app.get("/metrics")
def get_metrics():
    return {"routes": metrics}
