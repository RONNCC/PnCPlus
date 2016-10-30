from nltk.corpus import wordnet as wn
from nltk import pos_tag
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
wordnet_lemmatizer = WordNetLemmatizer()

def get_wordnet_pos(treebank_tag):

    if treebank_tag.startswith('J'):
        return wn.ADJ
    elif treebank_tag.startswith('V'):
        return wn.VERB
    elif treebank_tag.startswith('N'):
        return wn.NOUN
    elif treebank_tag.startswith('R'):
        return wn.ADV
    else:
        return ''

with open("test.txt", "rb") as f:
  for line in f:
    key_words = []
    #print pos_tag(word_tokenize(line))
    for (word, tag) in pos_tag(word_tokenize(line)):
      #print word, tag
      pos = get_wordnet_pos(tag)
      if(pos != ''):
	key_words.append(wordnet_lemmatizer.lemmatize(word, pos))
    print key_words

for synset in wn.synsets('stress'):
  print synset.lemmas()
