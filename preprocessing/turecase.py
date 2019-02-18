from collections import defaultdict


class TrueCase:
    """
    This class allow you to create a truecase model. the simplest one.
    https://en.wikipedia.org/wiki/Truecasing.
    """
    def __init__(self, modelfile, infile=''):
        """
        :modelfile: the file model.
        :infile: the file to train the model. If it's not given, the class will train a new model.
        """
        self.modelfile = modelfile
        self.infile = infile
        self.distribution_words = defaultdict(lambda: defaultdict(int))

        if self.infile:
            self.__train_truecase()
        else:
            self.__load_distribution()

    def __train_truecase(self):
        """
        :infile: path to the train data.
        return a model in modelfile.
        """
        train_file = open(self.infile, 'r', encoding=encoding_file(self.infile))
        sentences = [sentences.strip().split() for sentences in train_file.readlines()]        
        
        for sentence in sentences:
            for word in sentence:
                # {'pedro': {0: 1, 1: 20}, 'hola': 0:120, 1:3}
                self.distribution_words[word.lower()][word.istitle()] += 1

        model_file = open(self.modelfile, 'w', encoding='utf-8')
        for word, distribution in self.distribution_words.items():
            # dump a file with the distribution
            # word times_lower/times_upper
            model_file.write('{0} {1}/{2}\n'.format(word, distribution[0], distribution[1]))
        
        train_file.close()
        model_file.close()

    def __load_distribution(self):
        """"
        Load the model file to do truecasting.
        The model will be load onto distribution_words attribute.
        """
        with open(self.modelfile, 'r', encoding='utf') as f:
            word_distributions = map(lambda distribution: distribution.strip().split(' '), f.readlines())

        for word, distribution in word_distributions:
            lower, upper = distribution.split('/')
            self.distribution_words[word] = {0: lower, 1: upper}
    
    def is_upper(word):
        """
        This method will return if the word must be in upper
        :word: string
        return true if is an upper word.
        """
        return max(self.distribution_words[word].items(), lambda p: p[1])[0]
    
    def is_upper_sentence(sentence):
        """
        This method will return if the first word of the sentences
        should be in upper
        :sentence: string
        return  true if the first word of the sentences is upper
        """
        first_word = sentence.split(' ')[0]
        return self.is_upper(first_word)
    
    def upper_first_word(self, sentence):
        """
        This method will upper the first word of the sentence
        :sentence: string
        return the sentences with the first word uppered.
        """
        return sentence[0].upper() + sentence[1:]
    
    def true_case_sentence(self, sentence):
        """
        True case a single sentence with the distribution_words model.
        :sentence: a sequence of strings
        return a truecased sentence.
        """
        if self.is_upper_sentence(sentence):
            sentence = self.upper_first_word(sentence)
        return sentence

    def recaser_sentence(self, source_s, target_s):
        """
        The recaser will be depend on the source sentences.
        :source_s: source sentence.
        :target_s: target sentence.
        return a recase of the target sentence.
        """
        if self.is_upper_sentence(source_s):
            target_s = self.upper_first_word(target_s)
        return target_s