from sklearn.model_selection import train_test_split
from preprocessing import users
from loguru import logger
import shutil
import os


def train_dev_test_split(dev_size=0.1, test_size=0.1, set_to_split=None):
    if set_to_split is None:
        set_to_split = [str(val).zfill(3) + "-" + str(key) for key, val in users.items()]
    train, test = train_test_split(set_to_split, test_size=dev_size+test_size, random_state=69)
    dev, test = train_test_split(test, test_size=test_size/(dev_size+test_size), random_state=69)
    logger.info(f"Train: {sorted(train)} \n Dev: {sorted(dev)} \n Test: {sorted(test)}")
    logger.debug(f"Unsorted train: {train} \n Unsorted dev: {dev} \n Unsorted test: {test}")
    return train, dev, test


def get_split_from_json(json_path):
    import json
    with open(json_path) as f:
        data = json.load(f)
        return data["train"], data["dev"], data["test"]


def move_folders_to_split(split_json_path, source_folder):
    for folder in ['dev', 'test', 'train']:
        os.makedirs(os.path.join(source_folder, folder), exist_ok=True)
    train, dev, test = get_split_from_json(split_json_path)
    for folder in dev:
        logger.info(f"Moving {folder} to dev")
        shutil.move(os.path.join(source_folder, folder), os.path.join(source_folder, "dev"))
    for folder in test:
        logger.info(f"Moving {folder} to test")
        shutil.move(os.path.join(source_folder, folder), os.path.join(source_folder, "test"))
    for folder in train:
        logger.info(f"Moving {folder} to train")
        shutil.move(os.path.join(source_folder, folder), os.path.join(source_folder, "train"))


if __name__ == '__main__':
    split_path = "split/split.json"
    source_folder = "preprocessed"
    move_folders_to_split(split_path, source_folder)
