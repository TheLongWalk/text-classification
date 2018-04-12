from collections import OrderedDict
from operator import itemgetter 
import preprocessor
import advert_grouper
import json_parser
import argparse
import json

# creates a histogram of word counts from an advert-description map
def hist(descriptions):
    histogram = {}
    for advert in descriptions.values():
        for word in advert:
            if word in histogram:
                histogram[word] += 1
            else:
                histogram[word] = 1
    return histogram

# creates a histogram for each label
def groupHist(descriptions, groups):
    histograms = {}
    for label, adverts in groups.items():
        histogram = {}
        for advert in adverts:
            description = descriptions[advert]
            for word in description:
                if word in histogram:
                    histogram[word] += 1
                else:
                    histogram[word] = 1
        histograms[label] = histogram
    return histograms

if __name__ == '__main__':
    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--datapath', type=str, help="Input json file path")
    parser.add_argument('--labelpath', type=str, help="Input json file path")
    parser.add_argument('--target', type=str, default='paint', help="Target variable to group the adverts")
    args = parser.parse_args()

    # parse and preprocess advert descriptions
    descriptions = json_parser.parse(args.datapath, 'description', 'data')
    labels = json_parser.parse(args.labelpath, args.target, 'field')
    groups = advert_grouper.group(labels)

    # create histograms for each label
    preprocessor.preprocess(descriptions)
    histograms = groupHist(descriptions, groups)

    # sort the histograms in descending order
    for label, histogram in histograms.items():
        histograms[label] = OrderedDict(sorted(histogram.items(), key=itemgetter(1), reverse = True))

    # write the sorted histograms to a json file
    for label, histogram in histograms.items():
        dotPos = args.datapath.find('.')
        histogramFileName = args.datapath[:dotPos] + "-" + label + "-histogram.json"
        with open(histogramFileName, 'w') as fp:
            json.dump(histogram, fp)
