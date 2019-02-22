def which_encoding(infile):
    """
    :infile: guess the infile encoding.
    return {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
    """
    with open(infile, 'rb') as rawdata:
        result = chardet.detect(rawdata.read(10000))
    # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}
    return result['encoding']

def remove_s(sentence):
    return re.sub('</s>', '', sentence)

def remove_spaces(sentence):
    sentence = re.sub(' ,', ',', sentence)
    sentence = re.sub('« ', '«', sentence)
    sentence = re.sub(' »', '»', sentence)
    sentence = re.sub('\' ', '\'', sentence)
    sentence = re.sub(' :', ':', sentence)
    sentence = re.sub(' °', '°', sentence)
    sentence = re.sub(' - ', '-', sentence)
    sentence = re.sub(' x ', 'x', sentence)
    sentence = re.sub(' ’ ', '\'', sentence)
    sentence = re.sub(' / ', '/', sentence)
    sentence = re.sub('<\W*[0-9]*>', '', sentence)
    return sentence
