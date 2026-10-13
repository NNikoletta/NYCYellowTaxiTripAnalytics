import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

from pyspark.sql import SparkSession


def run_spark_pipeline():
    spark = (
        SparkSession.builder.appName("YellowTaxiTripAnalyticsApp").master("local[*]").getOrCreate()
    )

    data = [("exmp", 1), ("exmp", 2), ("exmp", 3), ("exmp", 4)]
    columns = ["Exmp", "Number"]

    df = spark.createDataFrame(data, schema=columns)
    df.show()

    spark.stop()
