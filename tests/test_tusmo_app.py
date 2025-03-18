"""
Script to start only all Unit tests
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

def run_tests():
    """
    Run all specified test files and return whether they pass.
    """
    test_files = [
        get_path("app/experiments/mode_duel_test.py"),
        get_path("app/experiments/mode_battleIA_test.py"),
        get_path("app/experiments/solveur_test.py"),
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"  # Force utf-8 encoding

    res = True
    for test_file in test_files:
        print(f"Running tests in {test_file}...")
        result = subprocess.run(
            [sys.executable, "-m", "unittest", test_file],
            capture_output=True,
            text=True,
            env=env,  # Use the updated environment
        )

        if result.returncode != 0:
            print(f"❌ Tests failed in {test_file}:")
            print(result.stdout)
            print(result.stderr)
            res = False
            continue

        print(f"✅ Tests passed in {test_file}.")

    return res


def test_flask_app():
    """
    Test the Flask application.
    """
    # Prepare environment variables
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"  # Force UTF-8 encoding

    print(f"Running tests in test_app.py...")

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
    if run_tests() and test_flask_app():
        print("✅ All tests passed")
    else:
        print("❌ Tests failed.")
