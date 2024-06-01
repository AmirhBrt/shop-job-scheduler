from src.runner import Runner

import sys

def main():
    config_file_path =  "./configs/config.json" if len(sys.argv) <= 1 else sys.argv[1]
    runner = Runner(config_file_path)
    runner.run()


if __name__ == '__main__':
    main()
