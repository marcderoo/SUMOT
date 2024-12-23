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


def start_flask_app():
    """
    Start the Flask application.
    """
    print("Running tests in start_test_app.py...")
    value=subprocess.run([sys.executable, "start_test_app.py"])
    if value.returncode == 0:
        print("✅ Tests passed in start_test_app.py .")
        return True
    else:
        print(f"❌ Tests failed in test_app.py:")
        return False


if __name__ == "__main__":
    results=run_tests() and start_flask_app()
    if results:
        print("✅ All tests passed")
    else:
        print("❌ Tests failed. Flask app will not start.")