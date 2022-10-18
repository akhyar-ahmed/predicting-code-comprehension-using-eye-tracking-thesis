# https://raw.githubusercontent.com/TheAlgorithms/Python/master/ciphers/mono_alphabetic_ciphers.py
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def translate_message(
    key: str, message: str, mode: Literal["encrypt", "decrypt"]
) -> str:
    chars_a = LETTERS if mode == "decrypt" else key
    chars_b = key if mode == "decrypt" else LETTERS
    translated = ""
    for symbol in message:
        if symbol.upper() in chars_a:
            sym_index = chars_a.find(symbol.upper())
            if symbol.isupper():
                translated += chars_b[sym_index].upper()
            else:
                translated += chars_b[sym_index].lower()
        else:
            translated += symbol
    return translated


def encrypt_message(key: str, message: str) -> str:
    return translate_message(key, message, "encrypt")
# # # # # delimiter # # # # # # #
print(encrypt_message("QWERTYUIOPASDFGHJKLZXCVBNM", "Well done"))
