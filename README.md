# Description
Exports an MS Excel file (.xlsx) with the fastest valid laps for each user in the given JSON file.

# Requirements
The JSON file must have no comments.

# Usage
You can run the code as usual. It requires one argument, which should be the relative path to the source JSON file.

Example: python src/main.py path/to/file.json

The application should create (or override) Excel files for each type of session (practice, qualifying and race) in the current directory.
