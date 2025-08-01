# src/libraryMS/data_processor.py

import os
import argparse
import pandas as pd
import logging
import json
from dotenv import load_dotenv

from schemas import MemberSchema, AuthorSchema, BookSchema, LibrarySchema

# Load environment variables
load_dotenv()

def setup_logger(log_level):
    logging.basicConfig(level=getattr(logging, log_level.upper()), format="%(levelname)s: %(message)s")

def process_file(file_path, schema):
    valid_records = []
    df = pd.read_csv(file_path, on_bad_lines='skip')
    df.columns = [col.lower().strip().replace(" ", "_") for col in df.columns]  # Normalize headers
    for i, row in df.iterrows():
        try:
            record = schema(**row.to_dict())
            logging.info(f"Row {i+1}: Valid")
            valid_records.append(record)
        except Exception as e:
            logging.warning(f"Row {i+1}: Invalid - {e}")
    return valid_records

def main():
    parser = argparse.ArgumentParser(description="Validate CSV data using Pydantic schemas.")
    parser.add_argument('--directory', '-d', default=os.getenv("DIRECTORY"), help='Directory containing CSV files')
    parser.add_argument('--log-level', default=os.getenv("LOG_LEVEL", "INFO"), help='Log level')
    args = parser.parse_args()

    setup_logger(args.log_level)

    files_to_process = {
        'members.csv': MemberSchema,
        'authors.csv': AuthorSchema,
        'books.csv': BookSchema,
        'libraries.csv': LibrarySchema,
    }

    for file_name, schema in files_to_process.items():
        file_path = os.path.join(args.directory, file_name)
        print("Current working directory:", os.getcwd())
        print("Looking for:", os.path.abspath(file_path))

        if os.path.exists(file_path):
            logging.info(f"Validating {file_name}...")
            valid_records = process_file(file_path, schema)
            logging.info(f"Validated {len(valid_records)} records in {file_name}.")

            # Save to output
            output_dir = os.path.join(os.path.dirname(__file__), "output")
            os.makedirs(output_dir, exist_ok=True)
            output_file = os.path.join(output_dir, file_name.replace(".csv", "_valid.json"))

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump([r.model_dump() for r in valid_records], f, indent=2)

            logging.info(f"Saved valid records to {output_file}")
        else:
            logging.warning(f"File {file_name} not found in directory {args.directory}")

if __name__ == "__main__":
    main()
