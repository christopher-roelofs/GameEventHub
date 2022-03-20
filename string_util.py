

def replace_value(value,tokens):
    for token in tokens:
        if value == f"{{{token}}}":
            value = tokens[token]
    return value


def replace_text(text,tokens):
    for token in tokens:
        if type(tokens[token]) == str:
            text = text.replace(f"{{{token}}}",tokens[token])
    return text
