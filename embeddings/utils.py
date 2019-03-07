import numpy as np


from sklearn.decomposition import TruncatedSVD


def compute_pc(X, npc=1):
    """
    Compute the principal components. DO NOT MAKE THE DATA ZERO MEAN!
    :param X: X[i,:] is a data point
    :param npc: number of principal components to remove
    :return: component_[i,:] is the i-th pc
    """
    svd = TruncatedSVD(n_components=npc, n_iter=7, random_state=0)
    svd.fit(X)
    return svd.components_

def remove_pc(X, npc=1):
    """
    Remove the projection on the principal components
    :param X: X[i,:] is a data point for a sentences
    :param npc: number of principal components to remove
    :return: XX[i, :] is the data point after removing its projection
    """
    pc = compute_pc(X, npc)
    if npc==1:
        XX = X - X.dot(pc.transpose()) * pc
    else:
        XX = X - X.dot(pc.transpose()).dot(pc)
    return XX

def save_word_embeddings(embeddings, file_to_dump):
    """
    dump the embeddings into a .txt file.
    :embeddings: the embeddings has to be an numpy type.
    """
    np.save(file_to_dump, embedding_deco, allow_pickle=False)

def load_word_embedding(file_to_load):
    """
    load word embeddings from a txt file.
    :file_to_load: a path to a file with the embeddings (.npy)
    return the embeddings with a numpy type
    """
    return np.load(file_to_load, allow_pickle=False)
