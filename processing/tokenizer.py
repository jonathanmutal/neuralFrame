import mosestokenizer

from processing.utils import remove_spaces

"""
TODO --- do a parent class.
"""

class Tokenizer:
    """
    This class will be a wrapper of MosesTokenizer.
    """
    def __init__(self, lang='en'):
        """
        :lang: lang for the tokenizer
        """
        self.__tokenizer = mosestokenizer.MosesTokenizer(lang)

    def tokenize_sentence(self, sentence):
        """
        :sentence: a string sentence.
        retun tokenized sentence.
        """
        return ' '.join(self.__tokenizer(sentence))

    def close(self):
        """
        Close the tokenizer
        """
        self.__tokenizer.close()


class Detokenizer:
    """
    This class will be a wrapper of MosesTokenizer.
    """
    def __init__(self, lang='en'):
        """
        :lang: lang for the detokenizer
        """
        self.__detokenizer = mosestokenizer.MosesDetokenizer(lang)

    def detokenize_sentence(self, sentence):
        """
        :sentence: a string sentence.
        retun detokenized sentences.
        """
        sentence_processed = self.__detokenizer(sentence.split(' '))
        sentence_processed = remove_spaces(sentence_processed)
        return sentence_processed

    def detokenize_sentences(self, sentences):
        """
        :sentences: a list of sentences
        return a detokenized sentence
        """
        return [self.detokenize_sentence(sent) for sent in sentences]

    def close(self):
        """
        Close the tokenizer
        """
        self.__detokenizer.close()
