from sklearn.model_selection import train_test_split
from preprocessing import users


def train_dev_test_split(dev_size=0.1, test_size=0.1, set_to_split=None):
    if set_to_split is None:
        set_to_split = [str(val).zfill(3) + "-" + str(key) for key, val in users.items()]
        print(set_to_split)
    train, test = train_test_split(set_to_split, test_size=dev_size+test_size, random_state=69)
    dev, test = train_test_split(test, test_size=test_size/(dev_size+test_size), random_state=69)
    return train, dev, test


if __name__ == '__main__':
    users_nrs = range(1, 61)
    dev_size = 0.1
    test_size = 0.1

    train, test = train_test_split(users_nrs, test_size=dev_size+test_size, random_state=42)
    dev, test = train_test_split(test, test_size=test_size/(dev_size+test_size), random_state=42)

    print(f"Train: {sorted(train)}")
    print(f"Dev: {sorted(dev)}")
    print(f"Test: {sorted(test)}")

    print(train_dev_test_split())