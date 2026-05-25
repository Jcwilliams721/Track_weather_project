## Track and Field Environmental Readiness Recommendation System

## Project Structure

## Scripts

### Track_weather_Project.py

**Purpose**: Production pipeline the receives weather condition data and runs multiple rule-based logics to generate training recommendations

**Workflow**:
1. Fetches 7-day weather forecast from Open-Meteo API for multiple trackfacilites throughout Kentucky
2. 2. Runs pre-set variables through rule-based logics based on values sent to generate a readiness score, risk level, and text based training recommendation.

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
- `openpyxl`: Excel file handling
- `openmeteo_requests`: Optional wrapper library for Open-Meteo API

## API Reference

**Open-Meteo API**: https://open-meteo.com/en/docs
- Free access (no authentication required)
- Generous rate limits for educational use
- Supports multiple weather variables and locations
