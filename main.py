from src.runner import Runner


def main():
    config_file_path = "./configs/config.json"
    runner = Runner(config_file_path)
    runner.run()


if __name__ == '__main__':
    main()
