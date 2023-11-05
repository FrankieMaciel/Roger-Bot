import re

def format_phrase(word_list):
    if not word_list:
        return ""

    # Capitalize a primeira palavra.
    formatted_phrase = word_list[0].capitalize()

    for word in word_list[1:]:
        # Remove espaços antes de vírgulas e outros sinais de pontuação.
        if re.match(r'[.,;!?]', word):
            formatted_phrase += word
        else:
            formatted_phrase += ' ' + word

    return formatted_phrase