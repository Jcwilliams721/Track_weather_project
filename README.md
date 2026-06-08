## Track and Field Environmental Readiness Recommendation System

## Technologies Used

|Technology|Purpose|
|---|---|
|Open-Meteo API|Weather Data Source|
|Python|Weather processing and recommendation generation|
|SQLAlchemy|Python-to-PostgreSQL integration|
|PostgreSQL|Database Storage|
|Power BI|Planned Data Visualization|

## ETL Process
**Extract**
- Pulls weather data from Open-Meteo API

**Transform**
- Generates readiness scores
- Generates risk levels
- Creates training recommendations

**Validate**
- Null value check
- Duplicate check
- Humidity range check

**Load**
- Load transformed data into PostgreSQL using SQLAlchemy
- To keep up with the constantly changing weather, the ETF pipeline will replace the exisitng table in PostgreSQL on every run to ensure that the information stored is as accurate and up-to-date as possible.

## Data Visualization
This project utilizes Microsoft Power BI as the visualization tool with data connected directly from postgreSQL. The goal of the visual is to provide information in an interactice nad user-friendly manner.

**Dashboard features include:**
- Live PostgreSQL connectivity
- Interactive filtering by location
- Daily average cards for temperature, humidity perentage, and readines scores for each available location
- Training Recommendation reporting

## Scripts

### Track_weather_Project.py

**Purpose**: Production pipeline the receives weather condition data and runs multiple rule-based logics to generate training recommendations

**Workflow**:
1. Fetches 7-day weather forecast from Open-Meteo API for multiple trackfacilites throughout Kentucky
2. Runs pre-set variables through rule-based logics based on values sent to generate a readiness score, risk level, and text based training recommendation.

**Usage**:
```bash
python Track_weather_Project.py
```


## Requirements

Install dependencies from `requirements.txt`:
```bash
pip install -r requirements.txt
```

Key libraries:
- `requests`: HTTP library for API calls
- `pandas`: Data manipulation and analysis
- `openmeteo_requests`: Optional wrapper library for Open-Meteo API

## API Reference

**Open-Meteo API**: https://open-meteo.com/en/docs
- Free access (no authentication required)
- Generous rate limits for educational use
- Supports multiple weather variables and locations

## Future Improvements

With amble time, the following components look to be added:
- Athlete/Event group specific logic
- Historical weather tracking
- Injury risk Prediction
- Dashboard Automation
