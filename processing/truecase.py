from processing.utils import which_encoding
from collections import defaultdict


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
        self.distribution_words = defaultdict(lambda: defaultdict(int))
        self.sentences = sentences

        if self.infile or self.sentences:
            self.__train_truecase()
        else:
            self.__load_distribution()

    def __train_truecase(self):
        """
        :infile: path to the train data.
        return a model in modelfile.
        """
        if self.infile:
            train_file = open(self.infile, 'r', encoding=which_encoding(self.infile))
            sentences = train_file.readlines()
            train_file.close()
        else:
            sentences = self.sentences

        assert(len(sentences) != 0)
        sentences = [sentence.strip().split() for sentence in sentences]

        for sentence in sentences:
            # if the first word is no capitalized, we don't have any doubt that
            # is not capitalized
            try:
                first_word= sentence[0]
            except IndexError:
                print('first_word out of range:', sentence)
                continue

            if not first_word.istitle():
                self.distribution_words[first_word.lower()][0] += 1

            try:
                sentence = sentence[1:]
            except IndexError:
                print('index out of range:', sentence, first_word)
                continue

            for word in sentence:
                # {'pedro': {0: 1, 1: 20}, 'hola': 0:120, 1:3}
                self.distribution_words[word.lower()][word.istitle()] += 1

        model_file = open(self.modelfile, 'w', encoding='utf-8')
        for word, distribution in self.distribution_words.items():
            # dump a file with the distribution
            # word times_lower/times_upper
            model_file.write('{0} {1}/{2}\n'.format(word, distribution[0], distribution[1]))

        model_file.close()

    def __load_distribution(self):
        """"
        Load the model file to do truecasting.
        The model will be load onto distribution_words attribute.
        """
        with open(self.modelfile, 'r', encoding='utf-8') as f:
            word_distributions = map(lambda distribution: distribution.strip().split(' '), f.readlines())

        for word, distribution in word_distributions:
            lower, upper = distribution.split('/')
            self.distribution_words[word] = {0: int(lower), 1: int(upper)}

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
        reutrn the first word of the sentence
        """
        return sentence.split(' ')[0]


    def is_upper_sentence(self, sentence):
        """
        This method will return if the first word of the sentences
        should be in upper
        :sentence: string
        return  true if the first word of the sentences is upper
        """
        first_word = self.get_first_word(sentence)
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
        return sentence[0].lower() + sentence[1:]

    def true_case_sentence(self, sentence):
        """
        True case a single sentence with the distribution_words model.
        :sentence: a sequence of strings
        return a truecased sentence.
        """
        if self.is_upper_sentence(sentence):
            sentence = self.upper_first_word(sentence)
        else:
            sentence = self.lower_first_word(sentence)
        return sentence

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
        first_word = self.get_first_word(source_s)
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
