import json
import argparse

# parses the desired field in a json file and returns a dictionary in which the keys are advert numbers
def parse(path, field):
    # read the json file
    adverts = json.load(open(path))
    try:
        # create a dictionary from the two lists of keys and values
        keys = [advert['uid'] for advert in adverts]
        values = [advert['data'][field] for advert in adverts]
        return dict(zip(keys, values))
    except KeyError:
        # handle the exception in case an invalid field has been specified
        print("'" + field + "' is an invalid field! Please select one of the following:")
        # print the valid fields of an advert
        for key in adverts[0]['data'].keys():
            print(key)
        # return an empty dictionary in order to avoid further exceptions
        return {}

if __name__ == '__main__':
    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help="Input json file path")
    parser.add_argument('--field', default='description', type=str, help="Advert field to be parsed")
    args = parser.parse_args()

    # print each item in the dictionary of results
    results = parse(args.path, args.field)
    for item in results.items():
        print(item)
