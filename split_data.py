from sklearn.model_selection import train_test_split

if __name__ == '__main__':
    users = range(1, 61)
    dev_size = 0.1
    test_size = 0.1

    train, test = train_test_split(users, test_size=dev_size+test_size, random_state=42)
    dev, test = train_test_split(test, test_size=test_size/(dev_size+test_size), random_state=42)

    print(f"Train: {sorted(train)}")
    print(f"Dev: {sorted(dev)}")
    print(f"Test: {sorted(test)}")