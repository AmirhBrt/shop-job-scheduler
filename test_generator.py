import os.path
import uuid
import random

from src.tests.maker import TestMaker


def main():
    for i in range(20):
        machines_count = random.randint(2, 7)
        jobs_count = random.randint(3, 10)
        file_name = f"test-{machines_count}-machines-{jobs_count}-jobs-{str(uuid.uuid4())}.json"
        file_dir = "./configs/"
        file_path = os.path.join(
            file_dir, file_name
        )
        maker = TestMaker(
            algorithm="johnson",
            machines_count=machines_count,
            jobs_count=jobs_count,
        )
        maker.create_test(file_path=file_path)


if __name__ == '__main__':
    main()
