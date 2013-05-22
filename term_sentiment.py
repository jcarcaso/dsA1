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
        Score the sentiment of the terms based on term scores
        params:
            f: tweet file containing tweet per line
            sentDict: Sentiment dictionary
            sentDict: newSents dictionary object to populated
    """
    for line in f.readlines():
        # Evaluate line by line. Convert the line to unicode
        t = json.loads(unicode(line))
        if 'text' not in t:
            # If the 'text' attribute isn't present skip the entry. It's a delete entry
            continue

        #userReg = re.compile('\@\w*')
        wordList = re.split("[\s,\.,\,,\!,\;,\:]", t['text'])
        total = 0
        newWords = {}
        numWords = 0
        for word in wordList:
            #if len(word.strip(" ")) > 0 and not userReg.match(word.strip(" ")):
            word = word.strip(" ")
            word = word.strip("\"")
            word = word.strip("'")
            if len(word) > 0:
                numWords+=1
                # Convert to lower and check if it's in the dict. if so add to total
                word = word.lower()
                if word in sentDict:
                    total+=sentDict[word]
                else:
                    # We found a new word, so flag it for later
                    newWords[word] = 1

        for word in newWords.keys():
            # Set/update the score values
            if word in newSents:
                pos,neg,ind,tot = getScoreValues(newSents[word], total)
            else:
                pos,neg,ind,tot = (float(0),float(0),float(0),float(total))

            if total > 0:
                pos+=1
            elif total < 0:
                neg+=1
            else:
                ind+=1
            newSents[word] = [pos,neg,ind,tot]

def getScoreValues(values,total=0):
    """ 
        Extract the score value from the term string
    """
    pos = values[0]
    neg = values[1]
    ind = values[2]
    tot = values[3]
    return (pos,neg,ind,tot+total)

def calculateScore(pos,neg,ind,tot):
    """
        return the score for a term:
        params: 
            pos: num positive terms associated with term
            neg: num negative terms associated with term
            ind: num indiffernt terms associated with term
            tot: sum of scores for tweets with term
    """
    score = None
    if neg != 0:
        if pos!=0:
            score = pos/neg
        elif ind!=0:
            score = -1*neg/ind
        else:
            score = -1*neg
    elif ind != 0:
        score = pos/ind
    else:
        score = pos

    #score = score*tot
    return score

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
        pos,neg,ind,tot = getScoreValues(newSents[word])
        score = calculateScore(pos,neg,ind,tot)
        print "%s %s" % (word.encode('utf-8'), score)

if __name__ == '__main__':
    main()
