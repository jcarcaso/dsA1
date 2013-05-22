import re
import sys
import json

def scoreHashTags(f):
    """
        Count the occurences of the terms
        params:
            f: tweet file containing tweet per line
            terms: terms dictionary to populate
        returns:
            HashTag Score Dictionary
    """
    hashtagReg = re.compile('(#\w+)')

    ret = {}
    for line in f.readlines():
        # Evaluate line by line. Convert the line to unicode
        t = json.loads(unicode(line))
        if 'entities' not in t or not t['entities']:
            # If the 'text' attribute isn't present skip the entry. It's a delete entry
            continue
        t = t['entities']
        if 'hashtags' not in t or not t['hashtags']:
            continue
        hashtags = t['hashtags']

        if len(hashtags) == 0:
            continue

        for hashtag in hashtags:
            hashtag = hashtag["text"]
            if hashtag in ret:
                ret[hashtag] += 1.0
            else:
                ret[hashtag] = 1.0

    return ret

def main():
    # Input
    tweet_file = open(sys.argv[1])
    # Actions
    hashTagDict = scoreHashTags(tweet_file)

    toptenscores = []
    topten = {}
    count = 0
    # Create our top ten list. It's simple, but not terribly efficient. 
    # We're only sorting 10 elements at a time, there's plenty of ways to 
    # make this more efficient
    # TODO Fix this to not have duplicates. I thin you were doing it right before.
    for tag in hashTagDict:
        score = hashTagDict[tag]
        if count < 10:
            count+=1
            toptenscores.append(score)
            toptenscores.sort(reverse=True)
            if score not in topten:
                topten[score] = [tag]
            else:
                topten[score].append(tag)
        else:
            if toptenscores[9] < score:
                oldscore = toptenscores[9]
                toptenscores[9] = score
                toptenscores.sort(reverse=True)
                if len(topten[oldscore]) == 1:
                    del topten[oldscore]
                elif len(topten[oldscore]) > 1:
                    topten[oldscore].pop()
                if score not in topten:
                    topten[score] = [tag]
                else:
                    topten[score].append(tag)

    # Print the top ten entries
    last = None
    for score in toptenscores:
        if score == last: 
            continue
        last = score
        for term in topten[score]:
            if len(term) > 0:
                print '%s %s' % (term, score)

if __name__ == '__main__':
    main()
