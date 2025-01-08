# Historical Travel Weather Analysis

This project analyzes historical weather data for different cities across multiple months. It provides temperature comparisons between cities based on historical data.

## Setup Instructions

### Prerequisites

- Python 3.11 or later
- `pip` for Python package management
- Git

### Installation Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/historical-travel-weather-analysis.git
    cd historical-travel-weather-analysis
    ```

2. Create a virtual environment (optional but recommended):
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

5. Use the API:

    Open Postman and import the Historical Travel Weather Analysis.postman_collection.json collection to interact with the API endpoints.
    The collection contains requests for querying weather data and other available API features.



