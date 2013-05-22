import re
import sys
import json

# States Regex
states = "AL|AK|AZ|AR|CA|CO|CT|DE|FL|GA|HI|ID|IL|IN|IA|KS|KY|LA|ME|MD|MA|MI|MN|MS|MO|MT|NE|NV|NH|NJ|NM|NY|NC|ND|OH|OK|OR|PA|RI|SC|SD|TN|TX|UT|VT|VA|WA|WV|WI|WY"
stateAbbr = re.compile(", (%s)$" % states)

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

def scoreStates(f, sentDict):
    """
        Score the sentiment of the tweets based on input and score the states based on that
        params:
            f: tweet file containing tweet per line
            sentDict: Sentiment dictionary
    """
    global states
    ret = {}
    for abbr in states.split("|"):
        ret[abbr] = 0

    for line in f.readlines():
        # Evaluate line by line. Convert the line to unicode
        t = json.loads(unicode(line))
        if 'text' not in t:
            # If the 'text' attribute isn't present skip the entry. It's a delete entry
            continue
        
        # Pull the state from our data. If no state, continue
        state = getState(t)
        if not state or state not in ret:
            continue

        wordList = re.split("[\s\.\,\!\;\:]", t['text'])
        for word in wordList:
            # Convert to lower and check if it's in the dict. if so add to total
            word = word.strip(" ").strip("\"").strip("'").lower()
            if word in sentDict:
                ret[state]+=sentDict[word]
    return ret

def getState(t):
    """
        return the state from a json tweet object. Return None otherwise
    """
    global stateAbbr
    for start,end in [('user', 'location'), ('place', 'name'), ('place', 'full_name')]:
        if start in t and t[start] and end in t[start] and t[start][end]:
            if stateAbbr.search(t[start][end]):
                return stateAbbr.search(t[start][end]).group(0)[2:].encode('utf-8')

    return None

def main():
    # Sentiment Object
    sentDict = {}
    # Input
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    # Actions
    createSentDict(sent_file, sentDict)
    scores = scoreStates(tweet_file, sentDict)

    happyState = None
    for s in scores:
        if not happyState or scores[s] > scores[happyState]:
            happyState = s
    print happyState.upper()

if __name__ == '__main__':
    main()
