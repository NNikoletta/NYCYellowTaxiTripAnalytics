---------------------------------------------------
---ATTRIBUTES AND DATA TYPES
---------------------------------------------------
---Exploring the columns and their types in 'trips'
DESCRIBE raw.trips;

SELECT * FROM raw.trips limit 2;

---Exploring the columns and their types in 'lookup'
DESCRIBE raw.lookup;

SELECT * FROM raw.lookup limit 2;

---------------------------------------------------
---NULL CELLS
---------------------------------------------------
SELECT * FROM (
    SELECT
        COUNT_IF(VendorID IS NULL) AS VendorID,
        COUNT_IF(tpep_pickup_datetime IS NULL) AS tpep_pickup_datetime,
        COUNT_IF(tpep_dropoff_datetime IS NULL) AS tpep_dropoff_datetime,
        COUNT_IF(passenger_count IS NULL) AS passenger_count,
        COUNT_IF(trip_distance IS NULL) AS trip_distance,
        COUNT_IF(RatecodeID IS NULL) AS RatecodeID,
        COUNT_IF(store_and_fwd_flag IS NULL) AS store_and_fwd_flag,
        COUNT_IF(PULocationID IS NULL) AS PULocationID,
        COUNT_IF(DOLocationID IS NULL) AS DOLocationID,
        COUNT_IF(payment_type IS NULL) AS payment_type,
        COUNT_IF(fare_amount IS NULL) AS fare_amount,
        COUNT_IF(extra IS NULL) AS extra,
        COUNT_IF(mta_tax IS NULL) AS mta_tax,
        COUNT_IF(tip_amount IS NULL) AS tip_amount,
        COUNT_IF(tolls_amount IS NULL) AS tolls_amount,
        COUNT_IF(improvement_surcharge IS NULL) AS improvement_surcharge,
        COUNT_IF(total_amount IS NULL) AS total_amount,
        COUNT_IF(congestion_surcharge IS NULL) AS congestion_surcharge,
        COUNT_IF(Airport_fee IS NULL) AS Airport_fee,
        COUNT_IF(cbd_congestion_fee IS NULL) AS cbd_congestion_fee
    FROM raw.trips
)
UNPIVOT(
    null_count FOR attribute_name IN (
            VendorID, tpep_pickup_datetime, tpep_dropoff_datetime, passenger_count, trip_distance, RatecodeID,
            store_and_fwd_flag, PULocationID, DOLocationID, payment_type, fare_amount, extra, mta_tax, tip_amount,
            tolls_amount, improvement_surcharge, total_amount, congestion_surcharge, Airport_fee, cbd_congestion_fee
    )
);

SELECT * FROM (
    SELECT
        COUNT_IF(LocationID IS NULL) AS LocationID,
        COUNT_IF(Borough IS NULL) AS Borough,
        COUNT_IF(Zone IS NULL) AS Zone,
        COUNT_IF(service_zone IS NULL) AS service_zone
    FROM raw.lookup
)
UNPIVOT(
    null_count FOR attribute_name IN (
            LocationID, Borough, Zone, service_zone
    )
);

---------------------------------------------------
---ANOMALIES
---------------------------------------------------
SELECT
    "dropoff_before_pickup" AS check_name,
    COUNT(*) AS invalid_row_count
FROM raw.trips
WHERE tpep_dropoff_datetime < tpep_pickup_datetime

UNION ALL

SELECT
    "outside_of_month",
    COUNT(*)
FROM raw.trips
WHERE tpep_pickup_datetime < '2025-01-01' OR tpep_pickup_datetime >= '2025-02-01'

UNION ALL

SELECT
    "trip_over_24h",
    COUNT(*)
FROM raw.trips
WHERE tpep_dropoff_datetime > tpep_pickup_datetime + INTERVAL 24 HOURS

UNION ALL

SELECT
    "zero_duration_trips",
    COUNT(*)
FROM raw.trips
WHERE tpep_pickup_datetime == tpep_dropoff_datetime

UNION ALL

SELECT
    "negative_total_amount",
    COUNT(*)
FROM raw.trips
WHERE total_amount < 0

UNION ALL

SELECT
    "negative_credit_card_charge",
    COUNT(*)
FROM raw.trips
WHERE total_amount < 0 AND payment_type == 1;
