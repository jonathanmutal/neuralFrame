import chardet


def encoding_file(infile):
    """
    :infile: guess the infile encoding.
    return {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
    """
    with open(infile, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(10000))
    # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
    return result['encoding']
