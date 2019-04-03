from processing.utils import which_encoding
from collections import defaultdict

from sacremoses import MosesTruecaser

class TrueCase:
    """
    This class allow you to create a truecase model. the simplest one.
    https://en.wikipedia.org/wiki/Truecasing.
    """
    def __init__(self, modelfile, sentences=[], infile=''):
        """
        :modelfile: the file model.
        :infile: sentences to train the model.
                 If it's not given, the class will train a new model.
        :sentences: list of sentences to train the model.
        """
        self.modelfile = modelfile
        self.infile = infile
        self.sentences = sentences

        if self.infile or self.sentences:
            self.__truecaser = self.__train_truecase()
        else:
            self.__truecaser = self.__load_truecaser()

    def __train_truecase(self):
        """
        :infile: path to the train data.
        return a model in modelfile.
        """
        sentences = self.sentences
        if self.infile:
            with open(self.infile, 'r', encoding=which_encoding(self.infile)) as train_file:
                sentences = train_file.readlines()

        assert(len(sentences) != 0)
        sentences = [sentence.strip().split() for sentence in sentences]
        mtr = MosesTruecaser()
        mtr.train(sentences, save_to=self.modelfile, processes=20, progress_bar=True)
        return mtr
        
    def __load_truecaser(self):
        """"
        Load the model file to do truecasting.
        The model will be load onto distribution_words attribute.
        """
        return MosesTruecaser(self.modelfile)  

    def is_upper(self, word):
        """
        This method will return if the word must be in upper
        :word: string
        return true if is an upper word.
        """
        return max(self.distribution_words.get(word.lower(), {0: 1, 1:0}).items(), key=lambda p: p[1])[0]

    def get_first_word(self, sentence):
        """
        get the first word from a sentence
        :sentence: string.
        reutrn the first word of the sentence and the remaining part in other list
        """
        sentence_splited = sentence.split(' ')
        first_word = sentence_splited[0]
        try:
            remaining = sentence_splited[1:]
            remaining = ' '.join(remaining)
        except IndexError:
            remaining = ''
        return first_word, remaining

    def is_upper_sentence(self, sentence):
        """
        This method will return if the first word of the sentences
        should be in upper
        :sentence: string
        return  true if the first word of the sentences is upper
        """
        first_word, _ = self.get_first_word(sentence)
        return self.is_upper(first_word)

    def upper_first_word(self, sentence):
        """
        This method will upper the first word of the sentence
        :sentence: string
        return the sentences with the first word uppered.
        """
        return sentence[0].upper() + sentence[1:]

    def lower_first_word(self, sentence):
        """
        This method will lower the first word of the sentence
        :sentence: string
        return the sentences with the first word lowered.
        """
        first_word, sentence = self.get_first_word(sentence)
        return first_word.lower() + ' ' + sentence

    def true_case_sentence(self, sentence):
        """
        True case a single sentence with the distribution_words model.
        :sentence: a sequence of strings
        return a truecased sentence.
        """
        return self.__truecaser.truecase(sentence, return_str=True)

    def true_case_sentences(self, sentences):
        """
        Truecase a list of sentences
        """
        return [self.true_case_sentence(sent) for sent in sentences]

    def recaser_sentence(self, source_s, target_s):
        """
        The recaser will be depend on the source sentences.
        :source_s: source sentence.
        :target_s: target sentence.
        return a recase of the target sentence.
        """
        first_word, _ = self.get_first_word(source_s)
        if first_word.istitle():
            target_s = self.upper_first_word(target_s)
        else:
            target_s = self.lower_first_word(target_s)
        return target_s


    def recaser_sentences(self, source_sents, target_sents):
        """
        Recase all the target sentences depend on source sentences.
        :source_sents: list of source sentences
        :target_sents: list of target sentences
        return a list of recases sentences
        """
        target_recase = []
        for source, target in zip(source_sents, target_sents):
            target_recase.append(self.recaser_sentence(source, target))
        return target_recase
