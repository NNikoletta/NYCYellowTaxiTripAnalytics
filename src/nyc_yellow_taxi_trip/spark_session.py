import os
import sys
from pathlib import Path

from nyc_yellow_taxi_trip.config import raw_data_dir

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession


def run_spark_pipeline(filename: str):
    spark = (
        SparkSession.builder.appName("YellowTaxiTripAnalyticsApp").master("local[*]").getOrCreate()
    )

    filepath = raw_data_dir / filename
    if not filepath.is_file():
        raise FileNotFoundError(f"'{filepath}' does not exist.")

    df = spark.read.parquet(str(filepath))
    df.createOrReplaceTempView("trips")

    df.printSchema(2)
    df.show(2)

    spark.stop()


def run_sql_file(spark, path):
    file_content = Path(path).read_text()
    statements = [s.strip() for s in file_content.split(";") if s.strip()]
    result = None
    for query in statements:
        result = spark.sql(query)
    return result
