


def replace_text(text,tokens):
    for token in tokens:
        if type(tokens[token]) == str:
            text = text.replace(f"{{{token}}}",tokens[token])
    return text
