import re
import sys
import json

def countTerms(f, terms):
    """
        Count the occurences of the terms
        params:
            f: tweet file containing tweet per line
            terms: terms dictionary to populate
        returns:
            total number of terms
    """
    totalTerms = 0
    for line in f.readlines():
        # Evaluate line by line. Convert the line to unicode
        t = json.loads(unicode(line))
        if 'text' not in t:
            # If the 'text' attribute isn't present skip the entry. It's a delete entry
            continue

        wordList = re.split("[\s,\.,\,,\!,\;,\:]", t['text'])
        for word in wordList:
            word = word.strip(" ")
            word = word.strip("\"")
            word = word.strip("'")
            if len(word) == 0:
                # Don't count the empty string
                continue 

            totalTerms+=1
            # Convert to lower and check if it's in the dict. if so add to total
            word = word.lower()
            if word in terms:
                terms[word]+=1
            else:
                terms[word]=1
                
    return totalTerms 

def main():
    terms={}
    # Input
    tweet_file = open(sys.argv[1])
    # Actions
    totalTerms = float(countTerms(tweet_file, terms))
    for t in terms:
        freq = terms[t]/totalTerms
        print "%s %s" % (t, freq)

if __name__ == '__main__':
    main()
