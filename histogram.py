from collections import OrderedDict
from operator import itemgetter 
import preprocessor
import json_parser
import argparse
import json

if __name__ == '__main__':
    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help="Input json file path")
    args = parser.parse_args()

    # parse and preprocess advert descriptions
    descriptions = json_parser.parse(args.path, 'description', 'data')
    preprocessor.preprocess(descriptions)

    # populate the histogram of word counts
    histogram = {}
    for key, advert in descriptions.items():
        for word in advert:
            if word in histogram:
                histogram[word] += 1
            else:
                histogram[word] = 1

    # sort the histogram in descending order
    histogram = OrderedDict(sorted(histogram.items(), key=itemgetter(1), reverse = True))

    # write the sorted histogram to a json file
    dotPos = args.path.find('.')
    histogramFileName = args.path[:dotPos] + "-histogram" + args.path[dotPos:]
    with open(histogramFileName, 'w') as fp:
        json.dump(histogram, fp)
