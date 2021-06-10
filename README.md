# Description
Exports an MS Excel file (.xlsx) with the fastest valid laps for each user in the given JSON file.

# Requirements
The JSON file must have no comments.

# Usage
You can run the code as usual. It requires one argument, which should be the relative path to the source JSON file.

Example:
```
python main.py <path/to/file.json>
```

The application should create (or override) Excel files for each type of session (practice, qualifying and race) in the current directory.

If you want to run the app directly, download [the compressed file containing binary](https://github.com/frdeazevedo/osr-json-excel-export/blob/master/dist/win10x64_v1.0.0-beta.zip), unzip it and run the following command on the terminal (in the same directory the binary file is placed):

```
main.exe <path/to/file.json>
```