import unicodedata
import re

def unicodeToAscii(s):
    return ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )

# Lowercase, trim, and remove non-letter characters
def normalizeString(s):
    # Remove espaços em branco extras do início e fim da string
    s = s.strip()
    
    # # Substitui caracteres acentuados por suas formas não acentuadas
    # s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    listWords = s.split(' ')
    listWords = [word.lower() for word in listWords]

    s = ' '.join(listWords)

    # Substitui caracteres de pontuação, exceto os específicos que queremos manter, por espaço
    s = re.sub(r"[!\"#$%&'()*/:;<=>?@[\\]^_`{|}~]", " ", s)

    # Substitui múltiplos espaços por um único espaço
    s = re.sub(r"\s+", " ", s)

    # Adiciona espaço antes dos caracteres específicos de pontuação que queremos manter
    s = re.sub(r"([.,!?])", r" \1", s)

    return s