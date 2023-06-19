def pad(text):
    padding_length = 8 - (len(text) % 8)
    padding = chr(padding_length) * padding_length
    return text + padding
