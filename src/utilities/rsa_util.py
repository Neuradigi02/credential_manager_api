import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization



with open("data/rsa_private_key.txt", "r") as file:
     private_key_str = file.read()

with open("data/rsa_public_key.txt", "r") as file:
     public_key_str = file.read()


class RSACipher(object):
    def __init__(self):
        self.private_key = serialization.load_pem_private_key(private_key_str.encode('utf-8'), password=None)
        self.public_key = serialization.load_pem_public_key(public_key_str.encode('utf-8'))
        

    def encrypt(self, plaintext):
        ciphertext = self.public_key.encrypt(
                     plaintext.encode(),
                     padding.OAEP(
                     mgf=padding.MGF1(algorithm=hashes.SHA256()),
                     algorithm=hashes.SHA256(),
                     label=None
            ))

        text = base64.b64encode(ciphertext).decode('utf-8')
        return text


    def decrypt(self,ciphertext):
            
            ciphertext_binary = base64.b64decode(ciphertext.encode('utf-8'))
            plaintext = self.private_key.decrypt(
            ciphertext_binary,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
            
            return plaintext.decode('utf-8')
    
            
rsa = RSACipher()