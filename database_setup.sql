CREATE TABLE athlete_group(
athlete_group_id SERIAL PRIMARY KEY,
group_name varchar(50)
);

INSERT INTO athlete_group(group_name)
VALUES
('Sprints'),
('Throws'),
('Distance')

CREATE TABLE training_recommendation(
    latitude FLOAT,
    longitude FLOAT,
    apparent_temperature FLOAT,
    humidity FLOAT,
    wind_speed FLOAT,
    wind_direction FLOAT,
    readiness_score INT, 
    risk_level VARCHAR(20), 
    recommendation TEXT
)

