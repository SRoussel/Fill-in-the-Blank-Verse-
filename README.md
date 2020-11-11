# M6 Poetry Slam - Fill in the Blank (Verse)

### A CSCI 3725 Project by Sam Roussel

#### Setup

This project uses a number of built-in packages, as well some which need to be installed:

    $ pip install beautifulsoup4
    $ pip install pronouncing
    $ pip install spacy
    $ pip install markovify

To run the program, execute the following from the project directory:

    $ python main.py
    
 ## Project Description
 This system generates blank verse, that is, un-rhymed metrical poetry (in this case, iambic pentameter). Such verse was
 popularized by Marlowe, and used often by Shakespeare, as well as by Milton in Paradise Lost. 
 
 This system creates a Markov model from a large corpus of over three million lines of poetry from
 Project Gutenberg, courtesy of Allison Parish: https://github.com/aparrish/gutenberg-poetry-corpus.
 
The system generates a number of lines; if they are iambic pentameter, they are kept. In addition, it uses
Veale's Metaphor Magnet to check if there is a metaphorical relation between a line and the next candidate line.
The candidate line is regenerated up to max_metaphor_attempts times or until there is a relation. This is meant to
provide a meaningful connection between lines.


 ## Creativity
 The system succeeds at generating iambic pentameter. The use of metaphor magnet does a lot to tie meaning between lines, but 
 there could be a lot of future work with seeding or evaluating future lines in different ways. 
 
 Markovify has built-in some important features, including checks that the text from the model does not resemble too closely the
 any text from the starting corpus. This is crucial in ensuring _originality_.
 
 Thus the poems are evaluated in a number of ways, from the originality checks to the iambic pentameter checks to the metaphorical
 relations score. These map nicely onto to the concepts of novelty, typicality, and quality. 

 ## Sources
 
 #### Technical
 [gutenberg corpus](https://github.com/aparrish/gutenberg-poetry-corpus)
    - a corpus of 3 million lines of poetry from the gutenberg project, used here to populate the Markov model.
    
 [spacy](https://spacy.io/) - POS tagging.
 
 [markovify](https://github.com/jsvine/markovify) - a convenient Markov model library.
 
 [metaphor magnet](http://bonnat.ucd.ie/metaphor-magnet-acl) - a web service which returns metaphorically related words for a given input.
 
 #### Scholarly
 
 [metaphor magnet](http://haddock.ucd.ie/Papers/ACL%20Veale%20and%20Li%202012.pdf) - Veale's work on the metaphor magnet.
 
 [POS tag ngrams](https://www.aclweb.org/anthology/W13-2121.pdf) - a similar technique, but using ngrams of grammatical relations. 
 
 [GPT 3.0](https://arxiv.org/pdf/2005.14165.pdf) - a cutting edge system using machine learning; quite impressive if not somewhat tangential.
 
