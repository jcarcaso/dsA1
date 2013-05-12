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

def scoreTerms(f, sentDict, newSents):
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

        userReg = re.compile('\@\w*')
        wordList = re.split("[\s,\.,\,,\!,\;,\:,\',\"]", t['text'])
        total = 0
        newWords = {}
        numWords = 0
        for word in wordList:
            if len(word.strip(" ")) > 0 and not userReg.match(word.strip(" ")):
                numWords+=1
                # Convert to lower and check if it's in the dict. if so add to total
                word = word.lower()
                if word in sentDict:
                    total+=sentDict[word]
                else:
                    newWords[word] = 1
        for word in newWords.keys():
            if word in newSents:
                #newSents[word]+= float(total)/numWords
                pos = int(newSents[word].split(":")[0])
                neg = int(newSents[word].split(":")[1])
                ind = int(newSents[word].split(":")[2])
                if total > 0:
                    pos+=1
                elif total < 0:
                    neg+=1
                else:
                    ind+=1
                newSents[word] = "%s:%s:%s" % (pos,neg,ind)
            else:
                #newSents[word] = float(total)/numWords
                pos = 0
                neg = 0
                ind = 0
                if total > 0:
                    pos+=1
                elif total < 0:
                    neg+=1
                else:
                    ind+=1
                newSents[word] = "%s:%s:%s" % (pos,neg,ind)

def main():
    # Sentiment Object
    sentDict = {}
    newSents = {}
    # Input
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    # Actions
    createSentDict(sent_file, sentDict)
    scoreTerms(tweet_file, sentDict, newSents)

    for word in newSents:
        #if newSents[word] != 0:
        #    print "%s %s" % (word.encode('utf-8'), newSents[word])
        pos = float(newSents[word].split(":")[0])
        neg = float(newSents[word].split(":")[1])
        ind = float(newSents[word].split(":")[2])
        if neg != 0:
            if pos!=0:
                print "%s %s" % (word.encode('utf-8'), pos/neg)
            elif ind!=0:
                print "%s %s" % (word.encode('utf-8'), -1*neg/ind)
            else:
                print "%s %s" % (word.encode('utf-8'), -1*neg)
        elif ind != 0:
            print "%s %s" % (word.encode('utf-8'), pos/ind)
        else:
            print "%s %s" % (word.encode('utf-8'), pos)

if __name__ == '__main__':
    main()
