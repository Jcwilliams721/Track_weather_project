import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below
url = "https://api.open-meteo.com/v1/forecast"
params = {
	"latitude": [38.216654818927914, 38.02855350938454, 36.98569946250266, 38.21579469876888, 37.736508914713504],
	"longitude": [-85.7534858144206, -84.49781402051626, -86.46059108007746, -85.70287524531375, -84.29839107702759],
	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "uv_index_max", "precipitation_hours", "wind_speed_10m_max", "wind_direction_10m_dominant"],
	"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "wind_speed_10m", "wind_direction_10m"],
	"wind_speed_unit": "mph",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
}
responses = openmeteo.weather_api(url, params = params)

def generate_recommendation(apparent_temp, humidity, wind_speed):

    readiness_score = 100
    risk_level = "Low"
    recommendations = []

    # Heat Logic
    if apparent_temp >= 95:
        readiness_score -= 40
        risk_level = "High"
        recommendations.append(
            "Reduce high-intensity sprint volume and emphasize hydration."
        )

    elif apparent_temp >= 85:
        readiness_score -= 20
        risk_level = "Moderate"
        recommendations.append(
            "Increase hydration and extend recovery periods."
        )

    else:
        recommendations.append(
            "Environmental conditions are suitable for normal training."
        )

    # Humidity Logic
    if humidity >= 70:
        readiness_score -= 15
        recommendations.append(
            "High humidity may increase heat stress and fatigue."
        )

    elif humidity >= 50:
        readiness_score -= 5
        recommendations.append(
            "Monitor hydration throughout practice."
        )

    # Wind Logic
    if wind_speed >= 20:
        readiness_score -= 20
        recommendations.append(
            "Strong winds detected. Modify throwing and sprint sessions."
        )

    elif wind_speed >= 10:
        readiness_score -= 10
        recommendations.append(
            "Moderate winds may affect sprint mechanics."
        )

    # Prevent negative scores
    readiness_score = max(readiness_score, 0)

    return readiness_score, risk_level, " | ".join(recommendations)

recommendation_results = []

# Process 5 locations
for response in responses:
    print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
	
	# Process current data. The order of variables needs to be the same as requested.
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_relative_humidity_2m = current.Variables(1).Value()
    current_apparent_temperature = current.Variables(2).Value()
    current_weather_code = current.Variables(3).Value()
    current_wind_speed_10m = current.Variables(4).Value()
    current_wind_direction_10m = current.Variables(5).Value()
	
    print(f"\nCurrent time: {current.Time()}")
    print(f"Current temperature_2m: {current_temperature_2m}")
    print(f"Current relative_humidity_2m: {current_relative_humidity_2m}")
    print(f"Current apparent_temperature: {current_apparent_temperature}")
    print(f"Current weather_code: {current_weather_code}")
    print(f"Current wind_speed_10m: {current_wind_speed_10m}")
    print(f"Current wind_direction_10m: {current_wind_direction_10m}")


	# Process daily data. The order of variables needs to be the same as requested.
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()
    daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
    daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
    daily_uv_index_max = daily.Variables(3).ValuesAsNumpy()
    daily_precipitation_hours = daily.Variables(4).ValuesAsNumpy()
    daily_wind_speed_10m_max = daily.Variables(5).ValuesAsNumpy()
    daily_wind_direction_10m_dominant = daily.Variables(6).ValuesAsNumpy()
	
    daily_data = {
    	"date": pd.date_range(
    		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
			end =  pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
			freq = pd.Timedelta(seconds = daily.Interval()),
			inclusive = "left"
		)
	}
	
    daily_data["weather_code"] = daily_weather_code
    daily_data["temperature_2m_max"] = daily_temperature_2m_max
    daily_data["temperature_2m_min"] = daily_temperature_2m_min
    daily_data["uv_index_max"] = daily_uv_index_max
    daily_data["precipitation_hours"] = daily_precipitation_hours
    daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
    daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

    readiness_score, risk_level, recommendation = generate_recommendation(
    current_apparent_temperature,
    current_relative_humidity_2m,
    current_wind_speed_10m)


    print(f"\nReadiness Score: {readiness_score}")
    print(f"Risk Level: {risk_level}")
    print(f"Recommendation: {recommendation}")

    recommendation_results.append({
        "latitude": response.Latitude(),
        "longitude": response.Longitude(),
        "apparent_temperature": current_apparent_temperature,
        "humidity": current_relative_humidity_2m,
        "wind_speed": current_wind_speed_10m,
        "wind_direction": current_wind_direction_10m,
        "readiness_score": readiness_score,
        "risk_level": risk_level,
        "recommendation": recommendation
})
    daily_dataframe = pd.DataFrame(data = daily_data)
    print("\nDaily data\n", daily_dataframe)

recommendation_df = pd.DataFrame(recommendation_results)

print("\nFinal Recommendation Table")
print(recommendation_df)

from sqlalchemy import create_engine

engine = create_engine(
    "postgresql://postgres:!75t!=DZHTWJCFM@localhost:1621/Track Project"
)

recommendation_df.to_sql(
    "training_recommendation",
    engine,
    if_exists="append",
    index=False
)
