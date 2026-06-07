import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry
from sqlalchemy import create_engine
import logging

logging.basicConfig(level=logging.INFO)

def extract_weather_data():    
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    url = "https://api.open-meteo.com/v1/forecast"

    param = {
    	"latitude": [38.216654818927914, 38.02855350938454, 36.98569946250266, 38.21579469876888, 37.736508914713504],
    	"longitude": [-85.7534858144206, -84.49781402051626, -86.46059108007746, -85.70287524531375, -84.29839107702759],
    	"daily": ["weather_code", "temperature_2m_max", "temperature_2m_min", "uv_index_max", "precipitation_hours", "wind_speed_10m_max", "wind_direction_10m_dominant", "apparent_temperature_max", "relative_humidity_2m_mean"],
    	"current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", "weather_code", "wind_speed_10m", "wind_direction_10m"],
    	"wind_speed_unit": "mph",
    	"temperature_unit": "fahrenheit",
    	"precipitation_unit": "inch",
    }
    responses = openmeteo.weather_api(url, params = param)
    return responses

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


def transform_weather_data(responses):

    recommendation_results = []

    try:

        # Process 5 locations
        for response in responses:

            # Process daily data
            daily = response.Daily()

            daily_weather_code = daily.Variables(0).ValuesAsNumpy()
            daily_temperature_2m_max = daily.Variables(1).ValuesAsNumpy()
            daily_temperature_2m_min = daily.Variables(2).ValuesAsNumpy()
            daily_uv_index_max = daily.Variables(3).ValuesAsNumpy()
            daily_precipitation_hours = daily.Variables(4).ValuesAsNumpy()
            daily_wind_speed_10m_max = daily.Variables(5).ValuesAsNumpy()
            daily_wind_direction_10m_dominant = daily.Variables(6).ValuesAsNumpy()
            daily_apparent_temperature_max = daily.Variables(7).ValuesAsNumpy()
            daily_relative_humidity_2m_mean = daily.Variables(8).ValuesAsNumpy()

            daily_data = {
                "date": pd.date_range(
                    start=pd.to_datetime(daily.Time(), unit="s", utc=True),
                    end=pd.to_datetime(daily.TimeEnd(), unit="s", utc=True),
                    freq=pd.Timedelta(seconds=daily.Interval()),
                    inclusive="left"
                )
            }

            daily_data["weather_code"] = daily_weather_code
            daily_data["temperature_2m_max"] = daily_temperature_2m_max
            daily_data["temperature_2m_min"] = daily_temperature_2m_min
            daily_data["uv_index_max"] = daily_uv_index_max
            daily_data["precipitation_hours"] = daily_precipitation_hours
            daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
            daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant
            daily_data["apparent_temperature_max"] = daily_apparent_temperature_max
            daily_data["relative_humidity_2m_mean"] = daily_relative_humidity_2m_mean

            for i in range (len(daily_apparent_temperature_max)):
                readiness_score, risk_level, recommendation = generate_recommendation(
                    daily_apparent_temperature_max[i],
                    daily_relative_humidity_2m_mean[i],
                    daily_wind_speed_10m_max[i]
            )
                recommendation_results.append({
                    "date": daily_data["date"][i],
                    "latitude": response.Latitude(),
                    "longitude": response.Longitude(),
                    "apparent_temperature": daily_apparent_temperature_max[i],
                    "humidity": daily_relative_humidity_2m_mean[i],
                    "wind_speed": daily_wind_speed_10m_max[i],
                    "readiness_score": readiness_score,
                    "risk_level": risk_level,
                    "recommendation": recommendation
            })
            print(f"\nCoordinates: {response.Latitude()}°N {response.Longitude()}°E")
            print(f"Elevation: {response.Elevation()} m asl")
            print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
            print(f"\nReadiness Score: {readiness_score}")
            print(f"Risk Level: {risk_level}")
            print(f"Recommendation: {recommendation}")
            daily_dataframe = pd.DataFrame(data=daily_data)

            print("\nDaily data\n", daily_dataframe)

    except Exception as e:

        logging.error(f"Transformation failed: {e}")
    
    recommendation_df = pd.DataFrame(recommendation_results)

    return recommendation_df

def validate_data(recommendation_df):
	logging.info("Running validation checks")


	recommendation_df = recommendation_df.drop_duplicates()
	#Null Check
	if recommendation_df.isnull().sum().sum() >0:
		logging.warning("Null values detectd")
	#duplicate check
	duplicates = recommendation_df.duplicated().sum()
	if duplicates >0:
		logging.warning(f"{duplicates} duplicate rows detected")
	#Humidity range check
	if recommendation_df["humidity"].max() > 100:
			logging.warning ("Invalid humidity values detectd")

	logging.info("Validation complete")


#def load_to_postgres(recommendation_df):
	logging.info("Loading data into PostgreSQL")
	try:
		engine = create_engine(
    		"postgresql://postgres:!75t!=DZHTWJCFM@localhost:1621/Track Project"
		)

		recommendation_df.to_sql(
    		"Daily_Recommendation",
    		engine,
    		if_exists="replace",
    		index=False
		)
		logging.info("Data loaded successfully")
	except Exception as e:
		logging.error(f"Database load failed: {e}")

def main():
	responses = extract_weather_data()
	recommendation_df = transform_weather_data(responses)
	validate_data(recommendation_df)
	print("\n Final Recommendation Table")
	print(recommendation_df)
	load_to_postgres(recommendation_df)


if __name__ == "__main__":
	main()
