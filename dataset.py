import json

if __name__ == '__main__':
    input = 'data/old_instances_25_30_35.json'
    output = 'data/new_instances_25_30_35_40.json'
    dataset = {}

    with open(input) as f:
        dataset = json.load(f)

    for j, level in enumerate(dataset):
        for i, instance in enumerate(dataset[level]):
            dataset[level][i]['hash'] = dataset[level][i]['id']
            dataset[level][i]['id'] = j * 50 + i

    with open(output, 'w') as f:
        json.dump(dataset, f)
