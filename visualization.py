import jsonpickle


def test():
    with open("results/test") as f:
        result = jsonpickle.decode(f.read())
        print(result["Partial scores"])


if __name__ == '__main__':
    test()
