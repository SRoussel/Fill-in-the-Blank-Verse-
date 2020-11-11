"""
A generator of blank verse, that is, metrical but un-rhyming poetry (in this case, iambic pentameter).

The system utilizes a Markov model created from a large corpus of over three million line of poetry from
Project Gutenberg, courtesy of Allison Parish: https://github.com/aparrish/gutenberg-poetry-corpus.

The system generates a number of lines; if they are iambic pentameter, they are kept. In addition, it uses
Veale's Metaphor Magnet to check if there is a metaphorical relation between a line and the next candidate line.
The candidate line is regenerated up to max_metaphor_attempts times or until there is a relation. This is meant to
provide a meaningful connection between lines.

@author Sam Roussel
"""

import gzip
import json
import os
import random
import re
import requests

# for web scraping of Metaphor Magnet
import bs4

# for syllables, stresses, and rhyming
import pronouncing

# POS tagging from https://spacy.io/
import spacy

# markov model from https://github.com/jsvine/markovify
import markovify


CORPUS_FILE = 'gutenberg-poetry-v001.ndjson.gz'
SPACY_MODEL = 'en_core_web_lg'
METAPHOR_URL = 'http://bonnat.ucd.ie/metaphor-magnet-acl/q?kw='


def generate_model(n=1000000):
    """
    Builds a markov model from the gutenberg poetry corpus.
    Markovify has some very nice features, including automatic checks that the generated output is sufficiently
    different from the starting text.
    """
    lines = []

    for line in gzip.open(CORPUS_FILE):
        lines.append(json.loads(line.strip()))

    # separate lines of poetry with newlines
    joined = '\n'.join([line['s'] for line in random.sample(lines, n)])

    # NewlineText uses newlines as "sentence" separators for the purposes of the model
    return markovify.NewlineText(joined)


def generate_text(model, num_lines=14, max_metaphor_attempts=5):
    """Generates a poem from the given markov model; also returns the score (more metaphorical relations are better)"""
    nlp = spacy.load(SPACY_MODEL)

    generated = []
    previous = None
    metaphor_attempts = 0
    score = num_lines

    while len(generated) < num_lines:
        line = model.make_sentence(tries=20, max_words=10, min_words=5)
        is_ten, line = make_ten_syllables(line)

        if is_ten and is_iambic_pentameter(line):
            # bail out if we've tried over max_metaphor_attempts times
            should_bail = metaphor_attempts > max_metaphor_attempts

            if should_bail or is_metaphorical(nlp, previous, line):
                # penalize if we've bailed out
                score -= 1 if should_bail else 0
                generated.append(line)
                previous = line
                metaphor_attempts = 0
            else:
                metaphor_attempts += 1

    return generated, score


def is_metaphorical(nlp, line, candidate):
    """Checks for a metaphorical relation between line and candidate according to the Metaphor Magnet"""
    if line is None:
        return True

    line_doc = nlp(line)
    candidate_doc = nlp(candidate)
    line_nouns = [token for token in line_doc if token.pos_ == 'NOUN']
    candidate_nouns = [token for token in candidate_doc if token.pos_ == 'NOUN']

    for noun in line_nouns:
        others = [other for other in candidate_nouns if other != noun]
        metaphors = get_metaphors(noun.text)

        for other in others:
            if other.text in metaphors:
                return True

    return False


def get_metaphors(tenor):
    """Uses Veale's Metaphor Magnet to find related words"""
    site = requests.get(METAPHOR_URL + tenor + '&xml=true')

    text = bs4.BeautifulSoup(site.text, 'lxml')
    words = text.find_all('source')

    vehicles = []

    for word in words:
        # @todo: utilize score in choosing
        score = word.find('score').string.strip()
        parts = word.find('text').string.strip().split(':')
        vehicles.append(parts[1])

    return vehicles


def is_iambic(syllables, stresses):
    """Checks whether the given stress pattern is iambic"""
    stress_string = ''
    
    # Since there may be multiple pronunciations of a syllable, take the stressed version if it exists
    for stress in stresses:
        if '1' in stress:
            stress_string = stress_string + '1'
        elif '2' in stress:
            stress_string = stress_string + '2'
        else:  # @todo: use regex to take the best candidate pronunciation
            stress_string = stress_string + stress[0]

    match = re.match('(.[12])+', stress_string)
    return match is not None and match.span()[1] - match.span()[0] == len(stress_string)


def is_iambic_pentameter(string):
    """Checks whether a line is iambic pentameter"""
    syllables = 0
    stresses = []
    for word in string.split():
        phones = pronouncing.phones_for_word(word)

        if not phones:
            return False

        count = pronouncing.syllable_count(phones[0])
        stresses.append(pronouncing.stresses_for_word(word))
        syllables += count

    # @todo: account for the common 11 syllable case (iambic pentameter preceded by a single soft syllable)
    return is_iambic(syllables, stresses) # and syllables == 10


def make_ten_syllables(line):
    """Recursively shortens a line into ten syllables if possible"""
    syllables = 0

    for word in line.split():
        phones = pronouncing.phones_for_word(word)

        if not phones:
            return False, line

        count = pronouncing.syllable_count(phones[0])
        syllables += count

    if syllables == 10:
        return True, line
    elif syllables > 10:
        return make_ten_syllables(' '.join(line.split()[:-1]))
    else:
        return False, line


def perform(poem):
    """Prints and recites the given poem line by line"""
    for line in poem:
        print(line)

    for line in poem:
        os.system('say -v Samantha ' + line)


def main():
    text, score = generate_text(generate_model())
    perform(text)
    print('Score: ' + score)


if __name__ == '__main__':
    main()
