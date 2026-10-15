# Profiling findings

**Status:** Draft - 0.1

**Project name:** NYC Yellow Taxi Trip Analytics

**Repository:** 'NNikoletta/NYCYellowTaxiTripAnalytics'

This file intends to document the findings of all the profiling queries that can be found in '[sql/profiling](https://github.com/NNikoletta/NYCYellowTaxiTripAnalytics/blob/master/docs/profiling_findings.md)'

## 1. 001_profile_raw_data.sql

To step into the next phase of the project, which is creating the staging tables, the raw data needs to be profiled to
gain complete understanding of it.

### Attributes and data types
The first two queries are responsible for exploring the columns and the data stored in them. The results are
the following:

* **Trips data:**
 
| col_name             | data_type | comment |
|----------------------|-----------|---------|
| VendorID             | int       | NULL    |
| tpep_pickup_datetime | timestamp | NULL    |
| tpep_dropoff_date... | timestamp | NULL    |
| passenger_count      | bigint    | NULL    |
| trip_distance        | double    | NULL    |
| RatecodeID           | bigint    | NULL    |
| store_and_fwd_flag   | string    | NULL    |
| PULocationID         | int       | NULL    |
| DOLocationID         | int       | NULL    |
| payment_type         | bigint    | NULL    |
| fare_amount          | double    | NULL    |
| extra                | double    | NULL    |
| mta_tax              | double    | NULL    |
| tip_amount           | double    | NULL    |
| tolls_amount         | double    | NULL    |
| improvement_surch... | double    | NULL    |
| total_amount         | double    | NULL    |
| congestion_surcharge | double    | NULL    |
| Airport_fee          | double    | NULL    |
| cbd_congestion_fee   | double    | NULL    |

| VendorID | tpep_pickup_datetime | tpep_dropoff_datetime | passenger_count | trip_distance | RatecodeID | store_and_fwd_flag | PULocationID | DOLocationID | payment_type | fare_amount | extra | mta_tax | tip_amount | tolls_amount | improvement_surcharge | total_amount | congestion_surcharge | Airport_fee | cbd_congestion_fee |
|----------|----------------------|-----------------------|-----------------|---------------|------------|--------------------|--------------|--------------|--------------|-------------|-------|---------|------------|--------------|-----------------------|--------------|----------------------|-------------|--------------------|
| 1        | 2025-01-01 00:18:38  | 2025-01-01 00:26:59   | 1               | 1.6           | 1          | N                  | 229          | 237          | 1            | 10.0        | 3.5   | 0.5     | 3.0        | 0.0          | 1.0                   | 18.0         | 2.5                  | 0.0         | 0.0                |
| 1        | 2025-01-01 00:32:40  | 2025-01-01 00:35:13   | 1               | 0.5           | 1          | N                  | 236          | 237          | 1            | 5.1         | 3.5   | 0.5     | 2.02       | 0.0          | 1.0                   | 12.12        | 2.5                  | 0.0         | 0.0                |

Inspecting the instances as well as the set data types, one can see that the first two examples match the data types
defined by the architecture. This makes it reasonable to believe that every attribute is assigned the correct data type.
While other queries are needed to ensure there are no empty cells in the tables and the values are consistent,
when creating the staging tables, the data types can be preserved from the raw table.

* **Lookup data:**
* 
| col_name     | data_type | comment |
|--------------|-----------|---------|
| LocationID   | string    | NULL    |
| Borough      | string    | NULL    |
| Zone         | string    | NULL    |
| service_zone | string    | NULL    |

| LocationID | Borough | Zone           | service_zone |
|------------|---------|----------------|--------------|
| 1          | EWR     | Newark Airport | EWR          |
| 2          | Queens  | Jamaica Bay    | Boro Zone    |

Unlike in the previous results, here one can notice that every attribute is assigned a string type, however the LocationID
is clearly an integer type. This attribute corresponds to the PU/DOLocation columns of the trips table
which are both integers. Based on the current observations and description of data on the TLC web page,
the LocationID attribute will be the base of a foreign key connection between the two tables. To make sure
this connection can be established, the type of the column needs to be converted to integer during staging.
In addition to this, due to its possible primary key nature, the attribute needs to be checked for duplicate as well as
null cells.

### Null cells

To ensure null constraints are added where needed, a null cells profiling is performed the results of which are
the following:

* **Trips data:**

| attribute_name       | null_count |
|----------------------|------------|
| VendorID             | 0          |
| tpep_pickup_datetime | 0          |
| tpep_dropoff_date... | 0          |
| passenger_count      | 540149     |
| trip_distance        | 0          |
| RatecodeID           | 540149     |
| store_and_fwd_flag   | 540149     |
| PULocationID         | 0          |
| DOLocationID         | 0          |
| payment_type         | 0          |
| fare_amount          | 0          |
| extra                | 0          |
| mta_tax              | 0          |
| tip_amount           | 0          |
| tolls_amount         | 0          |
| improvement_surch... | 0          |
| total_amount         | 0          |
| congestion_surcharge | 540149     |
| Airport_fee          | 540149     |
| cbd_congestion_fee   | 0          |

The null count data reveals quite a number of important observations. A total of five attributes have the same
number of null cells. This means this data was never recorded or reported and so can and this project will be 
handled as missing/incomplete data. When creating the staging tables, the null cells will be flagged as
'incomplete_record'. To determine which attributed require a not null constraint, it is crucial to understand
the data. While certain columns don't have any null records right now, they might have some the next month
(this project only focuses on data collected in January 2025, however, more data is available online).

Based on the data, attributed that cannot be null are the following: VendorID, tpep_pickup_datetime, tpep_dropoff_datetime,
trip_distance, PULocationID, DOLocationID, payment_type, fare_amount, total_amount. Without this information
the trip data cannot be valid.

* **Lookup data:**

| attribute_name | null_count |
|----------------|------------|
| LocationID     | 0          |
| Borough        | 0          |
| Zone           | 0          |
| service_zone   | 0          |

As expected due to the nature of the data stored in this table, it should not contain any null cells.

