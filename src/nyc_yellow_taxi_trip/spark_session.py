import logging
import os
import sys

from nyc_yellow_taxi_trip.config import project_root, raw_data_dir, sql_files_dir

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession

logger = logging.getLogger(__name__)


def run_spark_pipeline():
    spark = (
        SparkSession.builder.appName("YellowTaxiTripAnalyticsApp")
        .master("local[*]")
        .config("spark.sql.warehouse.dir", str(project_root / "spark-warehouse"))
        .enableHiveSupport()
        .getOrCreate()
    )
    trips_file = "yellow_tripdata_2025-01.parquet"
    lookup_file = "taxi_zone_lookup.csv"

    trips_path = raw_data_dir / trips_file
    lookup_path = raw_data_dir / lookup_file

    if not trips_path.is_file():
        raise FileNotFoundError(f"'{trips_path}' does not exist.")
    if not lookup_path.exists():
        raise FileNotFoundError(f"'{lookup_path}' does not exist.")

    trips_df = spark.read.parquet(str(trips_path))
    # trips_df.createOrReplaceTempView("trips")

    lookup_df = spark.read.csv(str(lookup_path), header=True)
    # lookup_df.createOrReplaceTempView("lookup")

    migrations_path = sql_files_dir / "migrations"
    run_sql_file(spark=spark, path=migrations_path / "001_create_schemas.sql")
    run_sql_file(spark=spark, path=migrations_path / "002_create_raw_tables.sql")
    trips_df.write.insertInto("raw.trips")
    lookup_df.write.insertInto("raw.lookup")

    profiling_path = sql_files_dir / "profiling"
    run_sql_file(spark=spark, path=profiling_path / "001_profile_raw_data.sql")

    spark.stop()


def run_sql_file(spark, path):
    with open(path, encoding="utf-8") as f:
        sql_content = f.read()

    statements = [s.strip() for s in sql_content.split(";") if s.strip()]
    for query in statements:
        try:
            result = spark.sql(query)
            result.show()
        except Exception as e:
            logger.exception(f"Failed to run query: {query}")
            raise e
