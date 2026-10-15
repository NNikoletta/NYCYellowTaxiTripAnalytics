import argparse
import logging
from collections.abc import Sequence

from nyc_yellow_taxi_trip.download_data import download_data
from nyc_yellow_taxi_trip.spark_session import run_spark_pipeline

logger = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nyc_yellow_taxi_trip",
        description="Download, transform, and analyze NYC Yellow Taxi Trip Data",
    )

    mode = parser.add_mutually_exclusive_group()

    mode.add_argument(
        "--download", action="store_true", help="Download raw NYC Yellow Taxi Trip Data."
    )

    mode.add_argument("--run-spark-session", action="store_true", help="Run Spark Session.")

    return parser


def main(argv: Sequence[str] | None = None) -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    args = build_parser().parse_args(argv)

    try:
        if args.download:
            download_data()
        elif args.run_spark_session:
            run_spark_pipeline()
        else:
            logger.info("Please choose a mode.")
    except Exception:
        logger.exception("Pipeline failed unexpectedly")
        raise
