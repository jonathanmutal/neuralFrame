from scipy.spatial.distance import cosine

def levenshtein_distance(str1, str2):
    """
    dynamic levenshtein distance.
    :str1: str1
    :str2: str2
    return the minimal edition between two strings.
    """
    d=dict()
    for i in range(len(str1)+1):
        d[i]=dict()
        d[i][0]=i
    for i in range(len(str2)+1):
        d[0][i] = i
    for i in range(1, len(str1)+1):
        for j in range(1, len(str2)+1):
            d[i][j] = min(d[i][j-1]+1, d[i-1][j]+1, d[i-1][j-1]+(not str1[i-1] == str2[j-1]))
    return d[len(str1)][len(str2)]

def cosine_similarity(vector1, vector2):
    """
    scipy compute the cosine distance and not cosine similarity, so that we
    add 1-cosine(v1, v2)
    return cosine_similarity
    """
    return 1 - cosine(vector1, vector2)
