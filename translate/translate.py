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
        self.tokenizer = lambda sent: Tokenizer(lang).tokenize_sentence(sent) if tokenizer else id
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
            sent_proces = self.tokenizer(sent)
            sent_proces = self.truecaser.true_case_sentence(sent)
            sent_proces = self.bpe.subword_sentence(sent) + '\n'
            sentences_proces.append(sent_proces)
        translated_sentences = self.translator.infer(sentences_proces)
        translated_sentences = self.bpe.de_subwords_sentences(translated_sentences)
        translated_sentences = self.truecaser.recaser_sentences(sentences, translated_sentences)
        translated_sentences = self.detokenizer.detokenize_sentences(translated_sentences)
        return neural_posprocessed(translated_sentences)

    def translate_file(self, path_in, path_out=''):
        """
        :path_in: path which are the sentences to translate.
        :path_out: path for the translated sentences. If doesn't
        give, just return the translated sentences
        return a list of translated sentences
        """
        with open(path_in, 'r') as f_in:
            sentences = list(map(lambda sent: sent.strip(), f_in.readlines()))

        translated_sentences = self.translate_sentences(sentences)
        if path_out:
            file_out = open(path_out, 'w')
            file_out.writelines([sent + '\n' for sent in translated_sentences])
            file_out.close()

        return translated_sentences

