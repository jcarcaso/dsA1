import re
import sys
import json

def createSentDict(f, sentDict):
    """
        Create the sentiment dictionary
        params:
            f: Sentiment file
            sentDict: Sentiment dictionary object to populate
    """
    for line in f.readlines():
        # We convert it to lower so we compare lowercase strings at all times
        sentDict[str(line.split('\t')[0]).lower()] = int(line.split('\t')[1])

def scoreTweets(f, sentDict):
    """
        Score the sentiment of the tweets based on input
        params:
            f: tweet file containing tweet per line
            sentDict: Sentiment dictionary
    """
    for line in f.readlines():
        # Evaluate line by line. Convert the line to unicode
        t = json.loads(unicode(line))
        if 'text' not in t:
            # If the 'text' attribute isn't present skip the entry. It's a delete entry
            continue

        wordList = re.split("[\s,\.,\,,\!,\;,\:]", t['text'])
        total = 0
        for word in wordList:
            # Convert to lower and check if it's in the dict. if so add to total
            word = word.lower()
            if word in sentDict:
                total+=sentDict[word]
        print total

def main():
    # Sentiment Object
    sentDict = {}
    # Input
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    # Actions
    createSentDict(sent_file, sentDict)
    scoreTweets(tweet_file, sentDict)

if __name__ == '__main__':
    main()
