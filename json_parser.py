import json
import argparse

# parses the description fields of the adverts in the given json file
def parse(path):
    adverts = json.load(open(path))
    return [advert['data']['description'] for advert in adverts]

if __name__ == '__main__':
    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--filepath', type=str, help="Input json file path")
    args = parser.parse_args()

    descriptions = parse(args.filepath)
    for d in descriptions:
        print(d + "\n\n")
