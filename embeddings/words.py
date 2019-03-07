class IndexWords:
    """
    This class is to manage word indexing.
    A sentence would be understood by the algorithm as long as we map each word by 
    a number.
    """
    def __init__(self, sentences=[], vocabulary_file='', pad_word='<s>'):
        """
        :sentences: the sentences which contains most vocabulary.
                    It has to be a list of all the sentences.
        :vocabulary_file: pre-loaded vocabulary.
        :pad_word: a word which will padded.
        :begin: number you like to begin index
        """
        self.id2word = []
        self.word2id = dict()
        
        self.pad_word = pad_word

        self.vocabulary_file = vocabulary_file

        if sentences:
            self.__create_vocabulary_from_sentences(sentences)
        elif self.vocabulary_file:
            self.__load_vocabulary()

    @property
    def size(self):
        """Returns the number of entries of the vocabulary."""
        return len(self.id2word)

    def __add(self, token):
        self.word2id[token] = self.size
        self.id2word.insert(self.size, token)

    def __create_index(self, vocabulary):
        """
        :vocabulary: an order structure for indexing words.
        """
        for word in vocabulary:
            self.__add(word)

    def __load_vocabulary(self):
        """
        load the vocabulary from a file.
        """
        with open(self.vocabulary_file, 'r') as vocab:
            vocabulary = map(lambda word: word.rstrip(), vocab.readlines())

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
        return self.id2word

    def get_word(self, idx):
        """
        :idx: return a word from the idx.
        Will return empty string if the idx is not in the dictionary
        """
        return self.id2word[idx]

    def get_index(self, token):
        """
        :word: return an id from a word.
        Return -1 if the word is not in the dictionary
        """
        return self.word2id.get(token, -1)

    def is_in_vocab(self, token):
        return word in self.id2word
