import os
import time

from src.runner import Runner

import sys


def run_config(config_file_path):
    runner = Runner(config_file_path)
    runner.run()


def main():
    if len(sys.argv) <= 1:
        run_config("./configs/test-2-machines.json")
        return
    name = sys.argv[1]
    if os.path.isdir(name):
        files = [f for f in os.listdir(name)]
        for file in files:
            file_path = os.path.join(
                name, file
            )
            run_config(file_path)
            time.sleep(3)
    else:
        run_config(name)


if __name__ == '__main__':
    main()
