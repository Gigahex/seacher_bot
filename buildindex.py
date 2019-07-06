from PIL import Image
import pytesseract
import os
import re
import Stemmer
stemmer = Stemmer.Stemmer('russian')


class BuildIndex:
    def __init__(self, folder):
        self.folder = folder
        self.filenames = os.listdir(folder)
        self.file_to_terms = self.process_files()
        self.total_index = self.fullIndex()
		
#метод получающий на вход картинку и создающий словарь вида:
#{file:[word1, word2, ...]}
    def process_files(self):
        file_to_terms = {}
        for file in self.filenames:
            file_to_terms[file] = (pytesseract.image_to_string(Image.open(os.path.join(self.folder, file)), lang='rus')).lower()

            pattern = re.compile(r'[\W_]+')
            pattern_small_word = re.compile(r'\s\w{1,2}\s')
            file_to_terms[file] = pattern_small_word.sub(' ',file_to_terms[file])
       
            file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
            file_to_terms[file] = pattern_small_word.sub(' ',file_to_terms[file])
            file_to_terms[file] = pattern_small_word.sub(' ',file_to_terms[file])

            re.sub(r'[\W_]+','', file_to_terms[file])
        
            file_to_terms[file] = file_to_terms[file].split()
            file_to_terms[file] = [stemmer.stemWord(w) for w in file_to_terms[file]]
            print("Идёт индексирование файлов! Подождите.")
        return file_to_terms
#input = {file:[word]}
#output = {word: [file]}
    def fullIndex(self):
        total_index = {}
        for filename in self.file_to_terms.keys():
            for word in self.file_to_terms[filename]:
                if word in total_index.keys():
                    total_index[word].append(filename)
                else:
                    total_index[word] = [filename]
        print('Индексирование файлов завершено')
        return total_index



