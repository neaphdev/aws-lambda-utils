

import pyaes
import base64_custom as b64
import config as cfg
class CryptoUtil():

    def __init__(self):
        self.semilla = cfg.semilla_crypto_card

    def encript_word(self, word):

        byte_semilla = bytes(self.semilla, 'utf-8')
        aes = pyaes.AESModeOfOperationCTR(byte_semilla)
        word_enc_bytes = aes.encrypt(word)
        word_enc= b64.encode_b64(word_enc_bytes)
        return word_enc
    
    def decript_word(self, word_encripted):
        byte_semilla = bytes(self.semilla, 'utf-8')
        aes = pyaes.AESModeOfOperationCTR(byte_semilla)
        word_encripted_bytes = b64.decode_b64(word_encripted, encryptation=True)
        word = aes.decrypt(word_encripted_bytes)
        return str(word.decode("utf-8"))