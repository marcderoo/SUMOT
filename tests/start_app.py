import subprocess
import sys
import os


def run_tests():
    """
    Run all specified test files and return whether they pass.
    """
    test_files = [
        "mode_duel_test.py",
        "mode_battleIA_test.py",
        "solveur_test.py",
    ]

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"  # Force utf-8 encoding

    os.chdir("experiments") 
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
            return False

        print(f"✅ Tests passed in {test_file}.")

    return True


def test_flask_app():
    """
    Test the Flask application.
    """
    os.chdir("..") 
    # Prepare environment variables
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"  # Force UTF-8 encoding

    print(f"Running tests in test_app.py...")

    result = subprocess.run(
        [sys.executable, "-m", "unittest", "test_app.py"],
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
        print("Starting Flask app...")
        subprocess.run([sys.executable, "app.py"])
    else:
        print("❌ Tests failed. Flask app will not start.")