# Chessboard

## jupyget

The built-in `jupyget` module is used for sending HTML reports of jupyter notebooks to specified servers.

## `install_notebook_dependencies(notebook_path)`

The process of this function is as follows:
1. Open `notebook_path` as a JSON file
2. Extract all `import` statements with regex (`import X` or `from X import Y`)
3. Map library names to package names (TODO: CHANGE THIS SO THAT YOU DON'T NEED A DICT AND IT IS AUTOMATIC)
4. Install all required packages with pip

## jupyget(notebook_path: str, server_url: str = None)

1. Run `install_notebook_dependencies`
2. Generate HTML report
3. Get the filename of the HTML report (TODO: CHANGE THIS SO THAT YOU CAN GET HTML PATH RIGHT WHEN YOU GENERATE REPORT)
4. If server url provided, send POST request to server

## Testing `jupyget`

To test `jupyget`, first start the test server:
```python
python3 server.py 
```
Then, run the main.py program:
```python
python3 main.py
```
The HTML report will then be sent to the `received_reports` folder. 
