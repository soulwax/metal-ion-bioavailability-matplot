# File: check_environment.py

"""
Environment diagnostic script to check Python environment and package availability.
"""

import sys
import subprocess
import importlib.util


def check_python_version():
    """Check Python version."""
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print("-" * 50)


def check_virtual_env():
    """Check if running in virtual environment."""
    in_venv = hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    )
    print(f"Running in virtual environment: {in_venv}")
    if in_venv:
        print(f"Virtual env prefix: {sys.prefix}")
    print("-" * 50)


def check_pip():
    """Check pip version and location."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"Pip info: {result.stdout.strip()}")
    except subprocess.CalledProcessError as e:
        print(f"Pip check failed: {e}")
    print("-" * 50)


def check_package(package_name):
    """Check if a package is available."""
    spec = importlib.util.find_spec(package_name)
    if spec is not None:
        try:
            module = importlib.import_module(package_name)
            version = getattr(module, "__version__", "Unknown version")
            print(f"✓ {package_name}: Available (version: {version})")
            return True
        except ImportError as e:
            print(f"✗ {package_name}: Import failed - {e}")
            return False
    else:
        print(f"✗ {package_name}: Not found")
        return False


def install_package(package_name):
    """Attempt to install a package."""
    try:
        print(f"Attempting to install {package_name}...")
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package_name],
            capture_output=True,
            text=True,
            check=True,
        )
        print(f"✓ {package_name} installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install {package_name}: {e}")
        print(f"Error output: {e.stderr}")
        return False


def main():
    """Run all diagnostic checks."""
    print("=" * 60)
    print("PYTHON ENVIRONMENT DIAGNOSTIC")
    print("=" * 60)

    # Basic environment checks
    check_python_version()
    check_virtual_env()
    check_pip()

    # Required packages for the script
    required_packages = ["numpy", "matplotlib", "networkx"]

    print("CHECKING REQUIRED PACKAGES:")
    print("-" * 50)

    missing_packages = []
    for package in required_packages:
        if not check_package(package):
            missing_packages.append(package)

    if missing_packages:
        print(f"\nMISSING PACKAGES: {missing_packages}")
        print("-" * 50)

        install_choice = (
            input("Attempt to install missing packages? (y/n): ").lower().strip()
        )
        if install_choice == "y":
            for package in missing_packages:
                install_package(package)

            print("\n" + "=" * 60)
            print("RE-CHECKING PACKAGES AFTER INSTALLATION:")
            print("=" * 60)
            for package in required_packages:
                check_package(package)
    else:
        print("\n✓ All required packages are available!")

    print("\n" + "=" * 60)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
