import subprocess
import sys


def execute(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    result = process.returncode
    if result != 0:
        print("An error occurred while running {}".format(command))
        print("stdout: {}".format(stdout))
        print("stderr: {}".format(stderr))
        sys.exit(1)
    return {
        "result": result,
        "stdout": stdout.decode('utf-8').split('\n'),
        "stderr": stderr.decode('utf-8').split('\n')
    }
