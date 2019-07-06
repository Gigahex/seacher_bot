import buildindex
import re, os
import Stemmer
stemmer = Stemmer.Stemmer('russian')
class Query:

    def __init__(self, folder):
        self.folder = folder
        self.index = buildindex.BuildIndex(self.folder)
        self.invertedIndex = self.index.total_index

    def one_word_query(self, word):
        word = word.lower()
        pattern = re.compile(r'[\W_]+')
        word = pattern.sub(' ',word)
        word = stemmer.stemWord(word)
        if word in self.invertedIndex.keys():
            return self.invertedIndex[word]
        else:
            return []

    def many_text_query(self, string):
        pattern = re.compile(r'[\W_]+')
        string = pattern.sub(' ',string)
        result = []
        for word in string.split():
            result += self.one_word_query(word)
        return list(set(result))
    