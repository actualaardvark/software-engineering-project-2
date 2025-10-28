import json
import re
import subprocess
import sys
import os
import requests

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
    
    # Map import names to package names
    package_map = {
        'sklearn': 'scikit-learn',
        'cv2': 'opencv-python',
        'PIL': 'Pillow',
    }
    
    packages = [package_map.get(imp, imp) for imp in imports]
    
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

jupyget("test.ipynb", "localhost:3000")