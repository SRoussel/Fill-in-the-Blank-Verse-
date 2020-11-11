"""
Module to generate an ngram dictionary. This yielded results worse than Markovify,
so the final product uses that library instead.

@author Sam Roussel
"""

from string import punctuation


def sanitize(corpus):
    """Remove punctuation from a text"""
    # create translation table to remove punctuation
    translator = str.maketrans('', '', punctuation)
    return corpus.translate(translator).lower()


def generate_ngrams(words, n):
    """Generate a list of ngrams from a text"""
    ngrams = []

    words = sanitize(words).split()

    for i in range(len(words) - n + 1):
        ngrams.append(words[i:i + n])

    return ngrams


def build_ngrams_dict(ngrams):
    """Build a dictionary from a list of ngrams"""
    ngram_dict = {}

    for ngram in ngrams:
        key_sequence = ' '.join(ngram[:-1])
        next_word = ngram[-1]

        if key_sequence not in ngram_dict:
            ngram_dict[key_sequence] = {}

        if next_word not in ngram_dict[key_sequence]:
            ngram_dict[key_sequence][next_word] = 0

        ngram_dict[key_sequence][next_word] += 1

    return ngram_dict
