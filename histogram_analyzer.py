import argparse
import json
import json_parser as jp
import advert_grouper as ag
import histogram as hg

DEFAULT_HISTOGRAM = "labels418gc-histogram.json"
DEFAULT_LABELS = "labels418gc.json"

def entropy(histogram, advertsPerLabel):
    entropyMap = {}
    for word, wordsPerLabel in histogram.items():
        histogram[word] = {label:count / advertsPerLabel[label] for (label, count) in wordsPerLabel.items()}
        entropyMap[word] = {label:abs(freq - (sum(histogram[word].values()) - freq)) for (label, freq) in histogram[word].items()}
    return entropyMap

if __name__ == '__main__':
    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--histpath', type=str, default=DEFAULT_HISTOGRAM, help="histogram file path")
    parser.add_argument('--labelpath', type=str, default=DEFAULT_LABELS, help="label file path")
    parser.add_argument('--target', type=str, default='paint', help="Target variable to group the adverts")
    args = parser.parse_args()

    # parse and preprocess advert descriptions
    advertLabelMap = jp.parse(args.labelpath, args.target, 'field')
    labelAdvertMap = ag.group(advertLabelMap)

    # compute the number of adverts per label
    advertsPerLabel = {}
    for label, adverts in labelAdvertMap.items():
        advertsPerLabel[label] = len(adverts)

    # read the histogram from file
    histogram = json.load(open(args.histpath))
    hg.printHist(histogram)

    # print words with high entropy
    entropyMap = entropy(histogram, advertsPerLabel)
    for word, entropy in entropyMap.items():
        if sum(entropy.values()) > 3:
            print(word + " " + str(entropy))
