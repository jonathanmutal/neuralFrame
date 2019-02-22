class IndexWords:
    """
    This class is to manage word indexing.
    A sentence would be understood by the algorithm as long as we map each word by 
    a number.
    """
    def __init__(self, sentences, pad_word='<pad>'):
        """
        :sentences: the sentences which contains most vocabulary.
                    It has to be a list of all the sentences.
        """
        assert len(sentences) != 0

        self.id2word = dict()
        self.word2id = dict()
        
        self.pad_word = pad_word

        self.__create_index(sentences)


    def __create_index(self, sentences):
        """
        The main function where the magic comes up.
        """
        vocab = set()
        for sent in sentences:
            vocab.update(sent.split(" "))

        # inicializate the dict with the pad_word
        self.id2word[0] = self.pad_word
        self.word2id[self.pad_word] = 0
        # its the main loop which gives an index for each word
        for index, word in enumerate(vocab):
            self.id2word[index+1] = word
            self.word2id[word] = index+1

    def get_vocabulary(self):
        return self.word2id.keys()

    def get_word(self, idx):
        """
        :idx: return a word from the idx.
        ---
        Will return empty string if the idx is not in the dictionary
        """
        return self.word2id.get(idx, "")

    def get_index(self, word):
        """
        :word: return an id from a word.
        ---
        Return -1 if the word is not in the dictionary
        """
        return self.word2id.get(word, -1)

    def get_index_word(self):
        return self.id2word.items()
