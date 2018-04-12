from collections import OrderedDict
from operator import itemgetter 
import preprocessor
import advert_grouper as ag
import json_parser as jp
import argparse
import json

LABELS = ['wasted', 'repaired', 'unknown', 'clean']

# creates a histogram of word counts from a list of descriptions
def hist(descriptionList):
    histogram = {}
    for description in descriptionList:
        for word in description:
            if word in histogram:
                histogram[word] += 1
            else:
                histogram[word] = 1
    return histogram

# creates a histogram for each label
def histLabels(advertDescriptionMap, labelAdvertMap):
    histogram = {}
    for label, adverts in labelAdvertMap.items():
        for advert in adverts:
            for word in advertDescriptionMap[advert]:
                if word in histogram:
                    if histogram[word][label] == None:
                        histogram[word][label] = 1
                    else:
                        histogram[word][label] += 1
                else:
                    histogram[word] = dict.fromkeys(LABELS)
                    histogram[word][label] = 1
    return histogram

if __name__ == '__main__':
    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--datapath', type=str, help="Input json file path")
    parser.add_argument('--labelpath', type=str, help="Input json file path")
    parser.add_argument('--target', type=str, default='paint', help="Target variable to group the adverts")
    args = parser.parse_args()

    # parse and preprocess advert descriptions
    advertDescriptionMap = jp.parse(args.datapath, 'description', 'data')
    advertLabelMap = jp.parse(args.labelpath, args.target, 'field')
    labelAdvertMap = ag.group(advertLabelMap)

    # create histograms for each label
    preprocessor.preprocess(advertDescriptionMap)
    histogram = histLabels(advertDescriptionMap, labelAdvertMap)

    # replace null values with zero
    for word, labelCountMap in histogram.items():
        for label in LABELS:
            labelCountMap[label] = labelCountMap[label] if labelCountMap[label] != None else 0
        histogram[word] = labelCountMap

    # print histogram
    for word, labelCountMap in histogram.items():
        print('{0: <25}'.format("\n" + word), end="")
        for label in LABELS:
            print('{0: >4}'.format(labelCountMap[label]), end="")
            print('{0: <10}'.format(" " + label), end="")

    # write histogram to a json file
    dotPos = args.labelpath.find('.')
    outFileName = args.labelpath[:dotPos] + "-histogram.json"
    with open(outFileName, 'w') as fp:
        json.dump(histogram, fp)
