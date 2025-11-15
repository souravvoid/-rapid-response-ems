import os
import sys
import subprocess
import platform

def run(cmd):
    print(f"[RUN] {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] Command failed: {cmd}")
        sys.exit(1)

def create_venv():
    venv_dir = "venv"
    python_exe = sys.executable

    if os.path.exists(venv_dir):
        print("Virtual environment already exists. Skipping creation.")
    else:
        print("Creating virtual environment...")
        run(f"{python_exe} -m venv venv")

    # OS-specific paths
    if platform.system().lower().startswith("win"):
        pip = os.path.join("venv", "Scripts", "pip")
        python = os.path.join("venv", "Scripts", "python")
    else:
        pip = os.path.join("venv", "bin", "pip")
        python = os.path.join("venv", "bin", "python")

    return pip, python

def install_requirements(pip):
    if os.path.exists("requirements.txt"):
        print("Installing dependencies...")
        run(f"\"{pip}\" install -r requirements.txt")
    else:
        print("No requirements.txt found. Skipping dependency installation.")

def run_project(python):
    # Auto-detect main file
    possible_files = ["main.py", "app.py", "run.py", "server.py"]

    for f in possible_files:
        if os.path.exists(f):
            print(f"Running {f}...")
            run(f"\"{python}\" {f}")
            return

    print("No runnable Python file found (main.py/app.py/run.py).")
    sys.exit(1)

def main():
    print("=== Automatic Setup Starting ===")

    pip, python = create_venv()
    install_requirements(pip)
    run_project(python)

    print("=== Setup Completed Successfully ===")

if __name__ == "__main__":
    main()
