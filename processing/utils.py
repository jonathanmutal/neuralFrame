import chardet
import re

from sacremoses import MosesPunctNormalizer

mosesNorm = MosesPunctNormalizer()

DATES = re.compile(r'\d{1,2}\/\d{1,2}\/\d{4}$|\d{1,2}\.\d{1,2}\.\d{4}')
LIST = re.compile(r'^([0-9][\.\-\)])+([0-9]+|/s)(?!([a-zA-Z]|\%))')
EMAIL = re.compile('[a-zA-Z0-9_\-\.]+@[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,6}')
LINK = re.compile('(http|ftp|https|www)(://)?([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?')


def turnLink(sent_s, sent_t):
    link = LINK.findall(sent_s)
    if link:
        link = ''.join(link[0])
        sent_t = re.sub('LINNK', link, sent_t)
        sent_t = re.sub('linnk', link, sent_t)
    return sent_t

def turnDates(sent_s, sent_t):
    date = DATES.findall(sent_s)
    if date:
        sent_t = re.sub('DAATTE', date[0], sent_t)
        sent_t = re.sub('daatte', date[0], sent_t)
    return sent_t

def turnEmail(sent_s, sent_t):
    email = EMAIL.findall(sent_s)
    if email:
        sent_t = re.sub('EEMMAIL', email[0], sent_t)
        sent_t = re.sub('eemmail', email[0], sent_t)
    return sent_t


def recoverEntity(sent_s, sent_t):
    return turnLink(sent_s, turnDates(sent_s, turnEmail(sent_s, sent_t)))

def recoverEntities(sents_s, sents_t):
    sents_pos_t = []
    for sent_s, sent_t in zip(sents_s, sents_t):
        sents_pos_t.append(recoverEntity(sent_s, sent_t))
    return sents_pos_t

def normalize(sentence):
    clean_sent = mosesNorm.normalize(sentence)
    return clean_sent


def turnApost(sentence):
    """
    turn all the Apostrophes to '.
    """
    clean_sentence =  re.sub(r'(\D)’', r'\1\'', sentence)
    return clean_sentence


def remove_number_list(sentence):
    """
    remove the number list
    """
    clean_sentence = cleanList.sub('', sentence)
    return clean_sentence


def cleanLinks(sentence):
    """
    clear all the links because they are useless.
    param is to clear sentences with just LINKS.
    """
    clean_sentence = LINK.sub('LINNK', sentence)
    return clean_sentence


def cleanDates(sentence):
    """
    This method turn all the dates to DAATTE label.
    """
    clean_sentence = DATES.sub('DAATTE', sentence)
    return clean_sentence


def cleanEmail(sentence):
    clean_sentence = EMAIL.sub('EEMMAIL', sentence)
    return clean_sentence


def descape(sentence):
    """
    :sentence: the sentence to be preprocessed.
    descape characters because the mosestokenizer will scape again.
    """
    sent = re.sub('&gt;', '>', sentence)
    sent = re.sub('&lt;', '<', sent)
    return re.sub('&amp;', '&', sent)


def neural_preprocessing(sentence):
    return normalize(cleanEmail(cleanDates(cleanLinks(descape(sentence)))))


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
    """
    Remove all the ocurrence </s>.
    :sentence: string
    """
    return re.sub('</s>', '', sentence)

def remove_spaces(sentence):
    """
    Remove all the spaces from a sentences.
    :sentence: string.
    """
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

def neural_posprocessed(sentences):
    """
    The posprocessed needed for neural system.
    :sentences: list of string
    """
    return list(map(lambda sent: remove_spaces(remove_s(sent)), sentences))
