from sacremoses import MosesTokenizer, MosesDetokenizer, MosesPunctNormalizer
from processing.utils import remove_spaces

"""
TODO --- do a parent class.
"""

class Tokenizer:
    """
    This class will be a wrapper of MosesTokenizer.
    """
    def __init__(self, lang='en', normalizer=True):
        """
        :lang: lang for the tokenizer
        """
        self.__tokenizer = MosesTokenizer(lang)

    def tokenize_sentence(self, sentence):
        """
        :sentence: a string sentence.
        retun tokenized sentence.
        """
        return self.__tokenizer.tokenize(sentence, return_str=True)

    def tokenize_sentences(self, sentences):
        """
        list of sentences to be tokenized
        :sentences: list of string
        """
        return [self.tokenize_sentence(sent) for sent in sentences]


class Detokenizer:
    """
    This class will be a wrapper of MosesTokenizer.
    """
    def __init__(self, lang='en'):
        """
        :lang: lang for the detokenizer
        """
        self.__detokenizer = MosesDetokenizer(lang)

    def detokenize_sentence(self, sentence):
        """
        :sentence: a string sentence.
        retun detokenized sentences.
        """
        sentence_processed = self.__detokenizer.detokenize(sentence.strip().split(' '))
        return sentence_processed

    def detokenize_sentences(self, sentences):
        """
        :sentences: a list of sentences
        return a detokenized sentence
        """
        return [self.detokenize_sentence(sent) for sent in sentences]

