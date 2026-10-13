import logging
from pathlib import Path

import requests
from tqdm import tqdm

from nyc_yellow_taxi_trip.config import raw_data_dir
from nyc_yellow_taxi_trip.utils import ensure_dir

logger = logging.getLogger(__name__)


def download_tlc_data(trip_type: str, year: int, month: int, output_dir: Path) -> None:
    """
    Downloads a specific NYC TLC trip parquet file.

    Parameters:
        trip_type (str): 'yellow', 'green', 'fhv', or 'hvfhv'
        year (int): year (e.g., 2025)
        month (int): month (e.g., 12)
        output_dir (str): destination folder for the downloaded files
    """

    ensure_dir(output_dir)
    filename = f"{trip_type}_tripdata_{year}-{month:02d}.parquet"
    url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/{filename}"
    file_path = Path(output_dir / filename)

    if file_path.is_file():
        logger.info(f"'{filename}' already exists and will not be overwritten. Skipping download.")
        return

    response = requests.get(url, stream=True)
    try:
        response.raise_for_status()  # Raises exception for HTTP errors

        total_size = int(response.headers.get("content-length", 0))

        logger.info(f"Downloading '{filename}' to '{output_dir}'")
        with (
            open(file_path, "wb") as f,
            tqdm(total=total_size, unit="B", unit_scale=True, desc=filename) as pbar,
        ):
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    pbar.update(len(chunk))
        logger.info("Download completed successfully.")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            logger.info(f"'{filename}' does not exist. Skipping download.")
        else:
            logger.info(f"HTTP Error: {e}")
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")


def download_lookup_csv() -> None:
    url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
    filename = "taxi_zone_lookup.csv"
    file_path = raw_data_dir / filename

    if file_path.is_file():
        logger.info(f"'{filename}' already exists and will not be overwritten. Skipping download.")
        return

    response = requests.get(url, stream=True)
    try:
        response.raise_for_status()
        logger.info(f"Downloading '{filename}' to '{raw_data_dir}'")
        with open(file_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        logger.info("Download completed successfully.")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            logger.info(f"'{filename}' does not exist. Skipping download.")
        else:
            logger.info(f"HTTP Error: {e}")
    except Exception as e:
        logger.info(f"An unexpected error occurred: {e}")


def download_data() -> None:
    download_tlc_data(trip_type="yellow", year=2025, month=1, output_dir=raw_data_dir)
    download_lookup_csv()
