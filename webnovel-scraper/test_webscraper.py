import subprocess
import sys


def run_webscraper(novel_name, novel_number, file_format):
    # Prepare the input as a single string, with newlines separating each input
    input_data = f"{novel_name}\n{novel_number}\n{file_format}\n"

    # Run the script and pass the input
    process = subprocess.Popen(
        ["python", "webscraper.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    # Communicate with the process, sending input and receiving output
    timeout = 180
    try:
        stdout, stderr = process.communicate(
            input_data, timeout=180
        )  # 5 minutes timeout
    except subprocess.TimeoutExpired:
        process.kill()
        stdout, stderr = process.communicate()
        print(f"Process timed out after {int(timeout/60)} minutes")

    return stdout, stderr


# Test cases
test_cases = [
    ("divine talisman", 1, "epub"),
    # ("another novel", 2, "q"),
]

for novel_name, novel_number, file_format in test_cases:
    print(f"Testing: {novel_name}, {novel_number}, {file_format}")
    stdout, stderr = run_webscraper(novel_name, novel_number, file_format)
    print("Output:", stdout)
    if stderr:
        print("Errors:", stderr)
    print("-" * 50)


sys.stdout.flush()
sys.stderr.flush()
