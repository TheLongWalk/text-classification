import json_parser as jp
import argparse
import re

# preprocesses and overwrites description strings from a map where the keys are advert numbers 
def preprocess(descriptions):
    for key, text in descriptions.items():
        # convert any uppercase letters to lowercase and normalize Turkish letters
        text = text.replace('İ', 'i').lower().replace('ş', 's').replace('ğ', 'g') \
                   .replace('ı', 'i').replace('ö', 'o').replace('ç', 'c').replace('ü', 'u')

        # replace any number, http(s) address and email address with the words 'number', 'httpaddr' and 'emailaddr'
        text = re.sub(r'[0-9]+', ' number ', text)
        text = re.sub('(http|https)://[^\s]*', 'httpaddr', text)
        text = re.sub('[^\s]+@[^\s]+', 'emailaddr', text)

        # split the text into words and get rid of any punctuation
        text = re.findall(r"[\w']+", text)

        # remove any non-alphanumeric characters and remove words with less than 2 letters
        for index, word in enumerate(text):
            word = re.sub('[^a-zA-Z0-9]', '', word)
            if (len(word) > 1):
                text[index] = word
            else:
                del text[index]

        # replace the raw description text with a preprocessed list of words
        descriptions[key] = text

if __name__ == '__main__':
    # parse program arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, help="Input json file path")
    args = parser.parse_args()

    # parse and preprocess advert descriptions
    descriptions = jp.parse(args.path, 'description', 'data')
    preprocess(descriptions)
    print(descriptions)
