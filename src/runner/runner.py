import json

from src.scheduler import RandomShopJobScheduler, JohnsonShopJobScheduler


class Runner:
    def __init__(self, file_path: str):
        self.file_path = file_path
        with open(file_path) as f:
            self.config = json.load(f)

    def run(self):
        if self.config["algorithm"] == "random":
            return RandomShopJobScheduler().schedule()
        elif self.config["algorithm"] == "johnson":
            return JohnsonShopJobScheduler().schedule()
