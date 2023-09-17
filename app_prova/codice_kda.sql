-- Creo tumbling window per ogni ora
CREATE OR REPLACE STREAM SensorDataWithHour AS
  SELECT STREAM
    STREAM_TIMESTAMP,
    eventtime,
    sensorid,
    temperature
  FROM sensortable
  WINDOWED BY
    TUMBLINGWINDOW(second, 3600);

-- Calcolo primo e terzo quartile per ogni sensore
CREATE OR REPLACE STREAM Quartiles AS
  SELECT STREAM
    eventtime,
    sensorid,
    temperature,
    FROM (SELECT *,
             row_number() over (ORDER BY temperature) as seqnum,
             COUNT(*) over () as cnt
      FROM sensortable)
    WHERE seqnum>= 0.25 * cnt and seqnum<= 0.75 * cnt;
  GROUP BY
    sensorid;

-- Calcolo media di temperatura per ogni ora
CREATE OR REPLACE STREAM AverageTemperature AS
  SELECT STREAM
    STREAM_TIMESTAMP AS Hour,
    sensorid,
    AVG(temperature) AS AvgTemperature
  FROM SensorDataWithHour AS S
  JOIN Quartiles AS Q
  ON S.sensorid = Q.sensorid
  WHERE S.temperature >= Q.PrimoQuartile
    AND S.temperature <= Q.TerzoQuartile;
  GROUP BY
    STREAM_TIMESTAMP,
    sensorid;



-- Inserisco dati in bucket
INSERT INTO 's3://sensordatabuckettrial123421432150F91F83/';
SELECT * FROM AverageTemperature;