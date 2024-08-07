# Spud Checker: The Spacemesh POST Potato Prober

## Overview

Spud Checker is a Python script designed to validate Spacemesh POST (Proof of Space-Time) data files. It uses the `postcli` tool to verify the integrity of POST data files and provides a user-friendly interface with a potato-themed output.

## Features

- Validates multiple POST data files in a specified directory
- Allows specification of the fraction of data to verify
- Provides a summary of validation results
- Outputs a CSV file listing any failed validations
- Optional debug logging for troubleshooting

## Requirements

- Python 3.6 or higher
- `postcli` executable (part of the Spacemesh toolset)
- Spacemesh POST data files

## Usage

```
python spud_checker.py <postcli_path> <data_dir> [--fraction FRACTION] [--debug]
```

### Arguments

- `postcli_path`: Path to the postcli executable
- `data_dir`: Path to the directory containing POST data files
- `--fraction`: Fraction of data to verify (default: 0.001)
- `--debug`: Enable debug logging (optional)

### Example

```
python spud_checker.py D:\postcli\postcli.exe \\NAS16A50A\spacemesh --fraction 0.001
```

## Output

The script provides real-time updates on the validation process:

```
🥔 Scrutinizing spud 0/3071...
🥔 Spud 0 is perfectly cooked. Validation successful!
🥔 Scrutinizing spud 1/3071...
🍟 Uh-oh! Spud 1 seems a bit crispy. Validation failed.
...
```

At the end of the process, a summary is provided, and a CSV file named `failed_validations.csv` is created in the data directory, listing any files that failed validation.

## Debugging

If you encounter issues or need more detailed information about the validation process, you can use the `--debug` flag:

```
python spud_checker.py D:\postcli\postcli.exe \\NAS16A50A\spacemesh --fraction 0.001 --debug
```

This will provide additional output, including the exact commands being run and their full output.

## Notes

- The script calculates the total number of files to check based on the `postdata_metadata.json` file in the data directory.
- Validation may take a significant amount of time, depending on the number of files and the fraction of data being verified.
- The script uses potato-themed emojis in its output. If these don't display correctly in your console, the script will still function normally.

## Troubleshooting

If you encounter any issues:

1. Ensure that the paths to `postcli` and the data directory are correct.
2. Check that you have the necessary permissions to access the data directory.
3. Verify that the `postdata_metadata.json` file is present and correctly formatted.
4. Run the script with the `--debug` flag for more detailed output.

If problems persist, please check the Spacemesh community forums or documentation for further assistance.

Happy potato probing! 🥔