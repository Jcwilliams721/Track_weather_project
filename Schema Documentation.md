# Database Schema Documentation

##Weather Forecast Data Warehouse

This database uses daily weeather data from the Open-Meteo API to generate training readiness recommendations for track and field athletes. Weather variables usch as apparent temperature, humidity, and wind speed are process in Python and stored in PostgreSQL for future analytics and visualization in Power BI.

---
### ER Diagram

(<img width="359" height="491" alt="ER_Diagram" src="https://github.com/user-attachments/assets/aafca789-fd92-464a-ae4c-31780d1e9306" />)

## Datbase Overview

The database contains 2 tables:

- `athlete_group`
- `training_recommendation`

## Table Documentation

| Table | Purpose|
|---|---|
|`athlete_group`| Stores specific event groups|
|`training_recommendation`| Stores weather conditions and generated readiness recommendations|

## Table 1: `athlete_group`

**Purpose**
Stores specific event groups

**Primary Key**

-One `athlete_group_id` can realte to many `training_recommendation records`

**Table Sructure**

|Column Name| Data Type| Key| Description |
|---|---|---|---|
|`athlete_group_id `|SERIAL| Priamry Key| Unique idntifier for athlete group|
|group+name| VARCHAR(50) | None | Name of athlete group |

**Example Data**

|`athlete_group_id` | `group_name`|
|---|---|
| 1 |Sprinters|
| 2 | Throwers|
| 3 | Distance |


## Table 2: `training_recommendation`

**Purpose**
Stores weather conditions, readiness scores, and generated training recommendations for multiple track facilites in Kentucky.

| Column Name | Data Type | Key Type| Description|
|---|---|---|---|
|recommendation_id|SERIAL|Primary Key|Unique recommendation identifier|
|latitude|FLOAT|None|Latitude of school location|
|longitude|FLOAT|None|Longitude of school location|
|apparent_temperature|FLOAT|None|Apparent temperature from weather API|
|humidity|FLOAT|None|Relative humidty percentage|
|wind_speed|FLOAT|None|Current wind speed|
|wind_direction|FLOAT|None|Wind direction in degrees|
|readiness_score|INT|None|Calculated environmental readiness score|
|risk_level|VARCHAR(20)|None|Environmental risk classification|
|recommendation|TEXT|None|Generated training recommendation|

---

## Relationships Between Tables
The athlete_group table is intended to support athlete specific recommendation logic. Future versions of the project may include athlete_group_id as a foreign key within the training_recommendation table to generate recommendations based on athlete type.

---

## Data Source

Weather forecast data is sourced from the Open-Meteo API.

The API provides:

- Daily apparent temperature
- Daily relative humidity
- Daily wind speed
- Daily wind direction

## Recommendation Source

Recommenations generated using rule-based logic based on weather data.

## Data Pipeline Explanation

Weather data is retrived using the Open-Meteo API through Python. Python processes the environment condtions and generated readiness recommendations using rule-based logic. The process results are exported to CSV format and imported PostegreSQL for storage and visualization.

## Future Improvements
Future improvements may include:
- Athlete specific recommednation logic
- Historical weather trackiung
- Automated PostegreSQL
- Live Power BI dashboard integration
- Injury risk prediction models
