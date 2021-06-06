# Description
Exports a MS Excel file (.xlsx) with the fastest valid laps for each user in the given JSON file.

# Requirements
The JSON file must have no comments.

# Usage
## If you have Python 3
You can run the code as usual. It requires one argument, which should be the relative path to the source JSON file.

Example: python src/main.py path/to/file.json

The application should create (or override) a file named **output.xlsx** in the current directory.