class IndexWords:
    """
    This class is to manage word indexing.
    A sentence would be understood by the algorithm as long as we map each word by 
    a number.
    """
    def __init__(self, sentences=[], vocabulary_file='', pad_word='<pad>', begin=0):
        """
        :sentences: the sentences which contains most vocabulary.
                    It has to be a list of all the sentences.
        :vocabulary_file: pre-loaded vocabulary.
        :pad_word: a word which will padded.
        :begin: number you like to begin index
        """
        self.id2word = dict()
        self.word2id = dict()
        
        self.pad_word = pad_word

        self.vocabulary_file = vocabulary_file
        self.begin = begin

        if sentences:
            self.__create_vocabulary_from_sentences(sentences)
        elif vocabulary_file:
            self.__load_vocabulary()

    def __create_index(self, vocabulary):
        """
        :vocabulary: an order structure for indexing words.
        """
        for index, word in enumerate(vocabulary, self.begin):
            self.id2word[index] = word
            self.word2id[word] = index

    def __load_vocabulary(self):
        """
        load the vocabulary from a file.
        """
        with open(self.vocabulary_file, 'r') as vocab:
            vocabulary = map(lambda word: word.strip(), vocab.readlines())

        self.__create_index(vocabulary)

    def __create_vocabulary_from_sentences(self, sentences):
        """
        The main function where the magic comes up.
        """
        vocab = set()
        for sent in sentences:
            vocab.update(sent.split(" "))
        vocabulary = [self.pad_word] + list(vocab)

        self.__create_index(vocab)

    def get_vocabulary(self):
        return self.word2id.keys()

    def get_word(self, idx):
        """
        :idx: return a word from the idx.
        Will return empty string if the idx is not in the dictionary
        """
        return self.word2id.get(idx, "")

    def get_index(self, word):
        """
        :word: return an id from a word.
        Return -1 if the word is not in the dictionary
        """
        return self.word2id.get(word, -1)

    def get_index_word(self):
        return self.id2word.items()
