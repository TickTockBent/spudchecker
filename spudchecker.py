#!/usr/bin/env python3
"""
Spud Checker: The Spacemesh POST Potato Prober
A script to validate Spacemesh POST data files
"""

import os
import json
import subprocess
import argparse
from pathlib import Path

def parse_metadata(data_dir):
    metadata_path = os.path.join(data_dir, "postdata_metadata.json")
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"🥔 Uh-oh! The postdata_metadata.json file is missing from {data_dir}")
    with open(metadata_path, 'r') as f:
        metadata = json.load(f)
    return metadata

def calculate_total_files(metadata):
    total_space = metadata['NumUnits'] * 64 * 1024 * 1024 * 1024  # NumUnits * 64 GiB in bytes
    return total_space // metadata['MaxFileSize']

def validate_file(postcli_path, data_dir, fraction, file_number, debug):
    command = [
        postcli_path,
        "-verify",
        "-datadir", data_dir,
        "-fraction", str(fraction),
        "-fromFile", str(file_number),
        "-toFile", str(file_number)
    ]
    if debug:
        print(f"[DEBUG] Executing command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    
    if debug:
        print(f"[DEBUG] Command output for file {file_number}:")
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
    
    # Combine stdout and stderr for checking
    full_output = result.stdout + result.stderr
    
    # Check for successful validation message
    if "cli: POS data is valid" in full_output:
        return True
    # Check for specific failure message
    elif "cli: invalid POS:" in full_output:
        return False
    else:
        print(f"🥔 Warning: Unexpected output for file {file_number}. Treating as failure.")
        return False

def confirm_execution(postcli_path, data_dir, fraction, total_files):
    print("\n🥔 Spud Checker: Confirmation Required")
    print(f"postcli path: {postcli_path}")
    print(f"Data directory: {data_dir}")
    print(f"Fraction to verify: {fraction}")
    print(f"Total files to validate: {total_files}")
    
    while True:
        response = input("\nAre you ready to start the potato probing? (yes/no): ").lower()
        if response in ['yes', 'y']:
            return True
        elif response in ['no', 'n']:
            return False
        else:
            print("Please answer with 'yes' or 'no'.")

def main(postcli_path, data_dir, fraction, debug):
    print("🥔 Spud Checker: Initiating potato-powered POST probing")
    
    # Check if paths exist
    if not os.path.exists(postcli_path):
        raise FileNotFoundError(f"🥔 Oops! The postcli executable wasn't found at {postcli_path}")
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"🥔 Oops! The data directory wasn't found at {data_dir}")
    
    try:
        metadata = parse_metadata(data_dir)
        total_files = calculate_total_files(metadata)
    except json.JSONDecodeError:
        raise ValueError(f"🥔 Oh no! The postdata_metadata.json file in {data_dir} is not valid JSON.")
    except KeyError as e:
        raise KeyError(f"🥔 Mashed potatoes! The postdata_metadata.json is missing a key: {str(e)}")
    
    if not confirm_execution(postcli_path, data_dir, fraction, total_files):
        print("🥔 Potato probing cancelled. Have a nice day!")
        return
    
    failed_files = []
    
    for file_number in range(total_files):
        print(f"🥔 Scrutinizing spud {file_number}/{total_files-1}...")
        if not validate_file(postcli_path, data_dir, fraction, file_number, debug):
            failed_files.append(file_number)
            print(f"🍟 Uh-oh! Spud {file_number} seems a bit crispy. Validation failed.")
        else:
            print(f"🥔 Spud {file_number} is perfectly cooked. Validation successful!")
    
    output_file = os.path.join(data_dir, "failed_validations.csv")
    with open(output_file, 'w') as f:
        f.write(",".join(map(str, failed_files)))
    
    print(f"🥔 Potato probing complete! Rotten spuds found: {len(failed_files)}")
    print(f"🥔 Results lovingly mashed into {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Spud Checker: Validate Spacemesh POST data with potato power")
    parser.add_argument("postcli_path", help="Path to the postcli executable")
    parser.add_argument("data_dir", help="Path to the data directory")
    parser.add_argument("--fraction", type=float, default=0.001, help="Fraction of potato to verify (default: 0.001)")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    
    args = parser.parse_args()
    
    try:
        main(args.postcli_path, args.data_dir, args.fraction, args.debug)
    except Exception as e:
        print(f"🥔 Oh no! A potato error occurred: {str(e)}")