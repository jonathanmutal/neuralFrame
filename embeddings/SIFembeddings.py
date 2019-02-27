"""
This module is inspired in https://github.com/PrincetonML/SIF
from this https://openreview.net/forum?id=SyK00v5xx paper.
"""
import numpy as np


from embeddings.utils import remove_pc


class SIFembeddings:
    """
    This is a wrapped class for SIFembeddings. It supposed to make easy
    our life
    """
    def __init__(self,
                 sentences,
                 word_embeddings,
                 word_id,
                 weightfile,
                 num_principal_component=1,
                 weightpara=1e-3,
                 a=1e-3):
        """
        :sentences: list of string with sentences.
        :word_embeddings: [size_vocab + 1, embeding_size] 
                         We[i,:] is the vector for word i.
        :word_id: a dict with word->id. It's a vocabulary.
        :weightfile: the distribution of the words.
        :weightpara: a parameter for the word weight.
        :a: the parameter for weight
        """
        self.word_id = word_id
        self.getWordWeight(weightfile, a)
        self.sentences2id(sentences)
        self.seq2weight()

        self.npc = num_principal_component
        self.We = word_embeddings
        self.SIF_embedding()

    def getWordWeight(self, weightfile, a=1e-3):
        """
        Get the paper word weight.
        :weightfile: a file with the distribution of the words.
        :return: each word weight.
        """
        if a <=0: # when the parameter makes no sense, use unweighted
            a = 1.0

        word2weight = {}
        # reading each word and deleting all \n
        lines = map(lambda word: word.strip().split(), weightfile.readlines())
        N = 0
        for word, freq in lines:
            word2weight[word] = float(freq)
            N += float(freq)
        index2weight = {}
        for word, value in word2weight.items():
            index2weight[self.word_id[word]] = a / (a + value/N)
        self.index2weight = index2weight

    def sentences2id(self, sentences):
        sentences_id = []
        for sentence in self.sentences:
            sentences_id.append([word_id[word] for word in sentence])
        self.sentences_id, self.masks = self.padd_sentences(sentences_id)

    def padd_sentence(self, sentence, max_length):
        sentence_id = np.zeros(max_length)
        mask = np.zeros(max_length)
        
        sentence_id[:len(sentence)] = sentence
        mask[:len(sentence)] = np.ones(len(sentence))
        return sentence_id, mask

    def padd_sentences(self, sentences_id):
        max_length = np.max([len(sent) for sent in sentences_id])

        sentences_padded_id, masks = [], []
        for sentence_id in sentences_id:
            sentence_padded_id, mask = padd_sentence(sentence_id, max_length)
            sentences_padded_id.append(sentence_padded_id)
            masks.append(mask)
        return np.array(sentences_padded_id), np.array(masks)

    def seq2weight(self):
        weight = np.zeros(self.sentences_id.shape).astype('float32')
        for i in range(self.sentences_id.shape[0]):
            for j in range(self.sentences_id.shape[1]):
                if self.masks[i,j] > 0 and self.sentences_id[i, j] >= 0:
                    weight[i,j] = self.index2weight[self.sentences_id[i, j]]
        weight = np.asarray(weight, dtype='float32')
        self.sentences_weight = weight

    def get_weighted_average(self):
        """
        Compute the weighted average vectors
        :param We: We[i,:] is the vector for word i
        :param x: x[i, :] are the indices of the words in sentence i
        :param w: w[i, :] are the weights for the words in sentence i
        :return: emb[i, :] are the weighted average vector for sentence i
        """
        n_samples = self.sentences_id.shape[0]
        embeding_size = self.We.shape[1]
        emb = np.zeros((n_samples, embeding_size))
        for i in range(n_samples):
            emb[i,:] = self.sentences_weight[i,:].dot(self.We[x[i,:],:]) / np.count_nonzero(self.sentences_weight[i,:])
        return emb

    def SIF_embedding(self):
        """
        Compute the scores between pairs of sentences using weighted average + removing the projection on the first principal component
        :return: emb, emb[i, :] is the embedding for sentence i
        """
        # return the average sentence
        emb = self.get_weighted_average()
        if  self.npc > 0:
            emb = remove_pc(emb, self.npc)
        return emb
