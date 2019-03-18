from processing.tokenizer import Tokenizer, Detokenizer
from processing.subword import Subword
from processing.truecase import TrueCase
from translatorMT.neural import Neural
from processing.utils import neural_posprocessed


class Translation:
    """
    This class will be in charge of translation a sentence with all
    the preprocessing and posprocessing.
    """
    def __init__(self, config, lang='en', tokenizer=True):
        """"
        All the files to do the pre-processing. First implementation.
        :config:
            - lang -- for the tokenizer.
            - truecase -- the truecase file.
            - codesfile -- the codesfile.
            - config_path -- path from the configuration files.
            - model_type -- the model name.
        """
        self.__config = config[lang]
        self.tokenizer = Tokenizer(lang) if tokenizer else id
        self.detokenizer = Detokenizer(lang)
        self.truecaser = TrueCase(modelfile=self.__config.get('truecasemodel'))
        self.bpe = Subword(codesfile=self.__config.get('codesfile'))
        self.translator = Neural(self.__config)

    def translate_sentences(self, sentences):
        """
        First implementation to translate.
        :sentences: list of sentences(strings)
        """
        sent_proces = ''
        sentences_proces = []
        for sent in sentences:
            sent_proces = self.tokenizer.tokenize_sentence(sent)
            sent_proces = self.truecaser.true_case_sentence(sent)
            sent_proces = self.bpe.subword_sentence(sent) + '\n'
            sentences_proces.append(sent_proces)
        translated_sentences = self.translator.infer(sentences_proces)
        translated_sentences = self.bpe.de_subwords_sentences(translated_sentences)
        translated_sentences = self.truecaser.recaser_sentences(sentences, translated_sentences)
        translated_sentences = self.detokenizer.detokenize_sentences(translated_sentences)
        return neural_posprocessed(translated_sentences)

    def close(self):
        self.detokenizer.close()
        self.tokenizer.close()
