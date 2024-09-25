from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

import base64


def _oaep_encrypt(message: bytes, public_key: RSA.RsaKey) -> bytes:
    cipher: PKCS1_OAEP.PKCS1OAEP_Cipher = PKCS1_OAEP.new(public_key, hashAlgo=SHA256)
    ciphertext: bytes = cipher.encrypt(message)
    return ciphertext


def _oaep_decrypt(ciphertext: bytes, private_key: RSA.RsaKey) -> bytes:
    cipher = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    plaintext: bytes = cipher.decrypt(ciphertext)
    return plaintext


def encrypt(plain_text: str, public_key: RSA.RsaKey) -> bytes:
    plain_text_in_bytes: bytes = bytes(plain_text, "utf-8")
    encrypted: bytes = _oaep_encrypt(plain_text_in_bytes, public_key)
    return base64.b64encode(encrypted)


def decrypt(base64_encoded_cipher_text: bytes, private_key: RSA.RsaKey) -> str:
    base64_decoded: bytes = base64.b64decode(base64_encoded_cipher_text)
    decrypted: bytes = _oaep_decrypt(base64_decoded, private_key)
    return decrypted.decode("utf-8")


def load_private_key(filepath: str) -> RSA.RsaKey:
    with open(filepath, "rb") as key_file:
        private_key = RSA.import_key(key_file.read())
    return private_key


# Example usage:
def main() -> None:
    # Generate RSA key pair
    # private_key = RSA.generate(2048)
    # public_key = key.publickey()

    private_key: RSA.RsaKey = load_private_key("private.pem")
    public_key: RSA.RsaKey = private_key.publickey()

    message: str = "Hello, World!"
    encrypted: bytes = encrypt(message, public_key)
    decrypted: str = decrypt(encrypted, private_key)

    print(f"Message:\n{message}\n")
    print(f"Encrypted (base64 encoded):\n{encrypted!r}\n")
    print(f"Decrypted (UTF-8):\n{decrypted}\n")


if __name__ == "__main__":
    main()
