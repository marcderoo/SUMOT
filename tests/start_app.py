"""
Script to start the application with all Unit tests
"""

import subprocess
import sys
import os

def get_path(full_path):
    """
    Get the full path of a file in the project.
    """
    root = os.path.dirname(os.path.abspath(__file__))
    # Go up until we find the LICENSE file
    while not os.path.exists(os.path.join(root, "LICENSE")):
        new_root = os.path.dirname(root)
        if new_root == root:  # Évite une boucle infinie
            raise FileNotFoundError("LICENSE file not found")
        root = new_root
    if "\\" in root :
        full_path = full_path.replace("/", "\\")
    else:
        full_path = full_path.replace("\\", "/")
    return str(os.path.join(root, full_path))

def test_flask_app():
    """
    Test the Flask application.
    """
    # Prepare environment variables
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"  # Force UTF-8 encoding

    print(f"Running tests in test_app.py...")
    print(f"RUNNING : {get_path('tests/test_app.py')}")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", get_path("tests/test_app.py")],
        capture_output=True,
        text=True,
        env=env,  # Use the updated environment
    )

    if result.returncode != 0:
        print(f"❌ Tests failed in test_app.py:")
        print(result.stdout)
        print(result.stderr)
        return False

    print(f"✅ Tests passed in test_app.py.")

    return True

if __name__ == "__main__":
    if test_flask_app():
        print("✅ All tests passed")
        print("Starting Flask app...")
        print(f"MAIN : {get_path('app/app.py')}")
        subprocess.run([sys.executable, get_path("app/app.py")])
    else:
        print("❌ Tests failed. Flask app will not start.")
