from pathlib import Path

import nyc_yellow_taxi_trip

project_root = Path(__file__).resolve().parents[2]

raw_data_dir = project_root / "data" / "raw"
sql_files_dir = project_root / "nyc_yellow_taxi_trip" / "sql"
