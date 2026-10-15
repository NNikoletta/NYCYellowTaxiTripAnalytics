CREATE TABLE IF NOT EXISTS staging.trips (
    VendorID INTEGER NOT NULL,
    tpep_pickup_datetime TIMESTAMP NOT NULL,
    tpep_dropoff_datetime TIMESTAMP NOT NULL,
    passenger_count BIGINT,
    trip_distance DOUBLE NOT NULL,
    RatecodeID BIGINT,
    store_and_fwd_flag STRING,
    PULocationID INTEGER NOT NULL,
    DOLocationID INTEGER NOT NULL,
    payment_type BIGINT NOT NULL,
    fare_amount DOUBLE NOT NULL,
    extra DOUBLE,
    mta_tax DOUBLE,
    tip_amount DOUBLE,
    tolls_amount DOUBLE,
    improvement_surcharge DOUBLE,
    total_amount DOUBLE NOT NULL,
    congestion_surcharge DOUBLE,
    Airport_fee DOUBLE,
    cbd_congestion_fee DOUBLE,

    CONSTRAINT fk_trips_pu_lookup FOREIGN KEY (PULocationID) REFERENCES staging.lookup (LocationID),
    CONSTRAINT fk_trips_do_lookup FOREIGN KEY (DOLocationID) REFERENCES staging.lookup (LocationID)
);

CREATE TABLE IF NOT EXISTS staging.lookup (
    LocationID INTEGER NOT NULL,
    Borough STRING NOT NULL,
    Zone STRING NOT NULL,
    service_zone STRING NOT NULL,

    CONSTRAINT pk_lookup PRIMARY KEY (LocationID)
);