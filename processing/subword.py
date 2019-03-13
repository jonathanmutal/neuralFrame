import codecs
import re


from subword_nmt.learn_bpe import learn_bpe
from subword_nmt.apply_bpe import BPE

from processing.utils import which_encoding

class Subword:
    """
    A subword-nmt wrapper.
    https://arxiv.org/abs/1508.07909.
    """
    def __init__(self, codesfile, trainfile='', num_symbols=32000, min_frequency=2, **config):
        """
        :codesfile: a file with the code
        :trainfile: if a trainfile is passed as an argument. The model will be training
        """
        self.__bpe = {}
        self.codesfile = codesfile
        self.trainfile = trainfile
        self.num_symbols = num_symbols
        self.min_frequency = min_frequency
        self.merges = config.get('merges', -1)
        self.codesfile = codesfile
        if not trainfile:
            codes = codecs.open(self.codesfile, encoding='utf-8')
            self.__bpe = BPE(codes, self.merges)
        else:
            self.__learn()

    def __learn(self):
        """
        Train a BPE.
        :trainfile: a file path which the model will learn.
        :codesfile: the output codes file.
        :num_symbols: number of vocabulary.
        :min_frequency: min frequency of the word.
        """
        trainfile = codecs.open(self.trainfile, encoding='utf-8')
        codesfile = codecs.open(self.codesfile, mode='w', encoding='utf-8')
        learn_bpe(trainfile, codesfile, self.num_symbols, self.min_frequency)
        self.__bpe = BPE(codes, self.merges)

    def subword_sentence(self, sentence):
        """
        :sentence: a list of words which will process.
        return a pre-proccesed sentences with bpe.
        """
        return self.__bpe.process_line(sentence)

    def subword_file(self, infile):
        """
        :infile: sentences in infile will be converted onto subwords
        it will generate a codes file with train_file.
        return a list of from preprocesed sentences from infile.
        """
        with open(infile, 'r', encoding=which_encoding(infile)) as f:
            sentences = f.readlines()
        return list(map(lambda sent: self.subword_sentence(sent.strip()), sentences))

    def de_subwords(self, sentence):
        """
        Removing the @@ for the sentence.
        :sentence: a sentence string
        """
        return re.sub('@@ ', '', sentence)

    def de_subwords_sentences(self, sentences):
        """
        List of sentence to remove @@
        :sentences: remove @@ for all the sentences in sentences
        """
        return list((map(self.de_subwords, sentences)))
