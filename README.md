# Chessboard

## jupyget

The built-in `jupyget` module is used for sending HTML reports of jupyter notebooks to specified servers.

TODO: add get package name to README

## `get_package_name(module_name)`

This function takes in module names as input and outputs their corresponding library names. The process of this function is as follows:
1. Use `fallback_map` for edge cases when mapping module names to package names
2. Get package name for a module with `importlib.metadata.distribution`
3. If submodule, get package name for the parent module
4. If not able to get the package name, fallback to the original module name 

## `install_notebook_dependencies(notebook_path)`

This function installs all required packages for a notebook. The process of this function is as follows:
1. Open `notebook_path` as a JSON file
2. Extract all `import` statements with regex (`import X` or `from X import Y`)
3. Map library names to package names
4. Install all required packages with pip

## jupyget(notebook_path: str, server_url: str = None)

This function runs a jupyter notebook, converts it to an HTML report, and sends it to a specified server. The process of this function is as follows:
1. Run `install_notebook_dependencies`
2. Generate HTML report
3. Get the filename of the HTML report 
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
