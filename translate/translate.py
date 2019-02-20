from processing.tokenizer import Tokenizer, Detokenizer
from processing.subword import Subword
from translatorMT.neural import Neural


class Translation:
    """
    This class will be in charge of translation a sentence.
    """
    def __init__(self, config):
        """"
        All the files to do the pre-processing. First implementation.
        :config:
            - lang -- for the tokenizer.
            - truecase -- the truecase file.
            - codesfile -- the codesfile.
            - config_path -- path from the configuration files.
            - model_type -- the model name.
        """
        self.__config = config
        self.tokenizer = Tokenizer(self.__config.get('lang', 'en'))
        self.detokenizer = Detokenizer(self.__config.get('lang', 'en'))
        self.truecaser = TrueCase(modelfile=config.get('truecasemodel'))
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
            sent_proces = self.bpe.subword_sentence(sent) + ['\n']
            sentences_proces.append(sent_proces)
        translated_sentences = self.translator.infer(sentences_proces)
        translated_sentences = self.bpe.de_subword_sentences(translated_sentences)
        translated_sentences = self.truecaser.recaser_sentences(sentences, translated_sentences)
        translated_sentences = self.detokenizer.detokenize_sentences(translated_sentences)
        return translated_sentences
