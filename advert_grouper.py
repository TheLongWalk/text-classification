import argparse
import json_parser as jp

# cretes a dictionary with 3 labels (keys) where the values are the corresponding list of adverts
def group(labels):
    groups = {}
    for advert, label in labels.items():
        if label == 'damage':
            label = 'wasted'
        elif label == '0':
            label = 'clean'
        elif label != 'unknown':
            label = 'repaired'

        if label not in groups:
            groups[label] = [advert]
        else:
            groups[label].append(advert)
    return groups

if __name__ == '__main__':
    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help="Input json file path")
    parser.add_argument('--target', type=str, default='paint', help="Target variable to group the adverts")
    args = parser.parse_args()

    # parse advert labels group the adverts by the specified target variable
    labels = jp.parse(args.path, args.target, 'field')
    groups = group(labels)
    for label, adverts in groups.items():
        print(label)
        for advert in adverts:
            print(advert)
        print()
