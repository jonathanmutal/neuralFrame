import mosestokenizer


class Tokenizer:
    """
    This class will be a wrapper of MosesTokenizer.
    """
    def __init__(self, tokenizer=True, lang='en'):
        """
        :lang: lang for the tokenizer
        :tokenize: true if you want to tokenize. Otherwise, it will be a detokenizer.
        """
        if tokenizer:
            self.__procesor = mosestokenizer.MosesTokenizer(lang)
        else:
            self.__procesor = mosestokenizer.DeTokenizer(lang)

    def tokenize_sentence(self, sentence):
        """
        :sentence: a string sentence.
        retun a tokenized sentences.
        """
        sentence_processed = self.__procesor(sentence)
        return ' '.join(sentence_processed)

    def close(self):
        """
        Close the tokenizer
        """
        self.__procesor.close()
