import gzip, os, re
import _cwordninja_core as core

__version__ = "2.0.0"

# I did not author this code, only tweaked it from:
# http://stackoverflow.com/a/11642687/2449774
# Thanks Generic Human!


# Modifications by Scott Randal (Genesys)
#
# 1. Preserve original character case after splitting
# 2. Avoid splitting every post-digit character in a mixed string (e.g. 'win32intel')
# 3. Avoid splitting digit sequences
# 4. Handle input containing apostrophes (for possessives and contractions)
#
# Wordlist changes:
# Change 2 required adding single digits to the wordlist
# Change 4 required the following wordlist additions:
#   's
#   '
#   <list of contractions>


class LanguageModel(object):
    def __init__(self, word_file):
        # Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
        if word_file.endswith(".gz"):
            with gzip.open(word_file) as f:
                words = f.read().decode().split()
        else:
            with open(word_file) as f:
                words = f.read().split()

        self._wordcost = core.make_wordcost(
            words
        )  # dict((k, log((i+1)*log(len(words)))) for i,k in enumerate(words))
        self._maxword = core.max_string_length(words)  # max(len(x) for x in words)

    def split(self, s):
        """Uses dynamic programming to infer the location of spaces in a string without spaces."""
        l = [self._split(x) for x in _SPLIT_RE.split(s)]
        for sublist in l:
            for item in sublist:
                yield item
    
    def lsplit(self, s):
        return list(self.split(s))

    def best_match(self, i, cost, s):
        return core.best_match(i, cost, self._wordcost, str(s), self._maxword)
    def _split(self, s):
        # Find the best match for the i first characters, assuming cost has
        # been built for the i-1 first characters.
        # Returns a pair (match_cost, match_length).
        '''
        def best_match(i):
            
            candidates = enumerate(reversed(cost[max(0, i - self._maxword) : i]))
            return min(
                (c + self._wordcost.get(s[i - k - 1 : i].lower(), 9e999), k + 1)
                for k, c in candidates
            )
        '''
        # Build the cost array.
        cost = [0.0]
        for i in range(1, len(s) + 1):
            c, k = self.best_match(i, cost, s)
            cost.append(c)

        # Backtrack to recover the minimal-cost string.
        out = []
        i = len(s)
        while i > 0:
            c, k = self.best_match(i, cost, s)
            # assert c == cost[i]
            # Apostrophe and digit handling (added by Genesys)
            newToken = True
            if not s[i - k : i] == "'":  # ignore a lone apostrophe
                if len(out) > 0:
                    # re-attach split 's and split digits
                    if out[-1] == "'s" or (
                        s[i - 1].isdigit() and out[-1][0].isdigit()
                    ):  # digit followed by digit
                        out[-1] = (
                            s[i - k : i] + out[-1]
                        )  # combine current token with previous token
                        newToken = False
            # (End of Genesys addition)

            if newToken:
                out.append(s[i - k : i])

            i -= k

        return reversed(out)


DEFAULT_LANGUAGE_MODEL = LanguageModel(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "wordninja_words.txt.gz")
)
_SPLIT_RE = re.compile("[^a-zA-Z0-9']+")


def split(s):
    return DEFAULT_LANGUAGE_MODEL.split(s)

def lsplit(s):
    return DEFAULT_LANGUAGE_MODEL.lsplit(s)
