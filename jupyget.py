import json
import re
import subprocess
import sys
import os
import requests
import importlib.metadata
import venv
import tempfile
import shutil

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

def install_notebook_dependencies(notebook_path, pip_executable):
    """Install notebook dependencies using a specific pip executable."""
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

    # Install all required packages with pip in the virtual environment
    if packages:
        subprocess.check_call([pip_executable, 'install'] + packages)

def jupyget(notebook_path: str, server_url: str = None):
    """
    Execute a Jupyter notebook in an isolated virtual environment and generate an HTML report.

    Args:
        notebook_path: Path to the Jupyter notebook (.ipynb file)
        server_url: Optional URL to POST the generated HTML report to
    """
    # Create a temporary directory for the virtual environment
    venv_dir = tempfile.mkdtemp(prefix='jupyget_venv_')

    try:
        print(f"Creating virtual environment at {venv_dir}...")

        # Create virtual environment
        venv.create(venv_dir, with_pip=True)

        # Determine paths to executables in the virtual environment
        if os.name == 'nt':  # Windows
            python_executable = os.path.join(venv_dir, 'Scripts', 'python.exe')
            pip_executable = os.path.join(venv_dir, 'Scripts', 'pip.exe')
        else:  # Unix/Linux/MacOS
            python_executable = os.path.join(venv_dir, 'bin', 'python')
            pip_executable = os.path.join(venv_dir, 'bin', 'pip')

        print("Installing Jupyter and nbconvert in virtual environment...")
        # Install jupyter, nbconvert, and ipykernel in the virtual environment
        subprocess.check_call([pip_executable, 'install', 'jupyter', 'nbconvert', 'ipykernel'])

        print("Installing notebook dependencies...")
        # Install notebook-specific dependencies
        install_notebook_dependencies(notebook_path, pip_executable)

        print("Creating Jupyter kernel...")
        # Create a kernel that points to this virtual environment
        kernel_name = f"jupyget_kernel_{os.path.basename(venv_dir)}"
        subprocess.check_call([
            python_executable, '-m', 'ipykernel', 'install',
            '--user', '--name', kernel_name,
            '--display-name', f'Python (jupyget)'
        ])

        print(f"Executing notebook with kernel {kernel_name}...")
        # Generate HTML report using the virtual environment's kernel
        subprocess.check_call([
            pip_executable.replace('pip', 'jupyter'),
            'nbconvert', '--to', 'html', '--execute',
            '--ExecutePreprocessor.kernel_name=' + kernel_name,
            notebook_path
        ])

        # Determine the output HTML file path
        html_path = notebook_path.rsplit('.', 1)[0] + '.html'
        print(f"HTML report generated: {html_path}")

        # If server URL is provided, send POST request
        if server_url:
            # Add http:// scheme if not present
            if not server_url.startswith(('http://', 'https://')):
                server_url = f'http://{server_url}'

            print(f"Sending report to {server_url}...")
            with open(html_path, 'r') as f:
                html_content = f.read()

            response = requests.post(server_url, data=html_content, headers={'Content-Type': 'text/html'})
            response.raise_for_status()
            print(f"Successfully sent HTML report to {server_url} (Status: {response.status_code})")

        # Clean up the kernel
        print(f"Cleaning up kernel {kernel_name}...")
        subprocess.run([
            pip_executable.replace('pip', 'jupyter'),
            'kernelspec', 'remove', '-f', kernel_name
        ], capture_output=True)

    finally:
        # Clean up the virtual environment
        print(f"Cleaning up virtual environment...")
        shutil.rmtree(venv_dir, ignore_errors=True)

