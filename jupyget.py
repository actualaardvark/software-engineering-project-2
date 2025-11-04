import json
import re
import subprocess
import sys
import os
import requests
import importlib.metadata

def get_package_name(module_name):
    """Automatically map module name to PyPI package name."""
    # Common edge cases that can't be auto-detected
    fallback_map = {
        'cv2': 'opencv-python',
        'PIL': 'Pillow',
    }

    if module_name in fallback_map:
        return fallback_map[module_name]

    try:
        # Try to get the distribution for the module
        return importlib.metadata.distribution(module_name).metadata['Name']
    except importlib.metadata.PackageNotFoundError:
        # Handle submodules (e.g., 'sklearn.metrics' -> 'scikit-learn')
        try:
            base_module = module_name.split('.')[0]
            return importlib.metadata.distribution(base_module).metadata['Name']
        except:
            pass

    return module_name  # Fallback to original name

def install_notebook_dependencies(notebook_path):
    # Parse notebook
    with open(notebook_path, 'r') as f:
        notebook = json.load(f)

    # Extract imports from code cells
    imports = set()
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = ''.join(cell.get('source', []))
            # Find imports: "import X" or "from X import"
            imports.update(re.findall(r'^\s*import\s+(\w+)', source, re.MULTILINE))
            imports.update(re.findall(r'^\s*from\s+(\w+)', source, re.MULTILINE))

    # Automatically map import names to package names
    packages = [get_package_name(imp) for imp in imports]

    # Install all required packages with pip
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)

def jupyget(notebook_path: str, server_url: str = None):
    install_notebook_dependencies(notebook_path)

    # Generate HTML report
    os.system("jupyter nbconvert --to html  --execute " + notebook_path)

    # Determine the output HTML file path
    html_path = notebook_path.rsplit('.', 1)[0] + '.html'

    # If server URL is provided, send POST request
    if server_url:
        # Add http:// scheme if not present
        if not server_url.startswith(('http://', 'https://')):
            server_url = f'http://{server_url}'

        with open(html_path, 'r') as f:
            html_content = f.read()

        response = requests.post(server_url, data=html_content, headers={'Content-Type': 'text/html'})
        response.raise_for_status()
        print(f"Successfully sent HTML report to {server_url} (Status: {response.status_code})")

