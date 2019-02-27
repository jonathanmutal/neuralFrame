def preprocessing(df, attribute):
    """
    This is the base preprocessing for french.
    It scapes \ char and replace all ocurrence of -
    :df: pandas data frame.
    :attribute: atribute of df.
    """
    return getattr(df, attribute).map(lambda sent: sent.lower().replace('\'', '\\\' ').replace('-', ' '))


def group(lst, n):
    """
    agroup the lst in subset of n elements.
    :lst: list
    :n: number of elements for subset
    """
    for i in range(0, len(lst), n):
        val = lst[i:i+n]
        if len(val) == n:
            yield list(val)
