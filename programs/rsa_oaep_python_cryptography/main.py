from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.padding import OAEP, MGF1
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

import base64


def load_private_key(file_path: str) -> RSAPrivateKey:
    """Load private key from PEM file"""

    with open(file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend(),
        )

    return private_key


def export_public_key(public_key: RSAPublicKey, output_filename: str) -> None:
    """Serialize the public key to PEM format"""

    pem: bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open(output_filename, "wb") as pem_out:
        pem_out.write(pem)


def _get_oaep() -> OAEP:
    return OAEP(
        mgf=MGF1(hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def _oaep_encrypt(plain_text: bytes, public_key: RSAPublicKey) -> bytes:
    encrypted: bytes = public_key.encrypt(plain_text, _get_oaep())
    return encrypted


def _oaep_decrypt(cipher_text: bytes, private_key: RSAPrivateKey) -> bytes:
    decrypted: bytes = private_key.decrypt(cipher_text, _get_oaep())
    return decrypted


def encrypt(plain_text: str, public_key: RSAPublicKey) -> bytes:
    plain_text_in_bytes: bytes = bytes(plain_text, "utf-8")
    cipher_text: bytes = _oaep_encrypt(plain_text_in_bytes, public_key)
    return base64.b64encode(cipher_text)


def decrypt(base64_encoded_cipher_text: bytes, private_key: RSAPrivateKey) -> str:
    base64_decoded: bytes = base64.b64decode(base64_encoded_cipher_text)
    decrypted: bytes = _oaep_decrypt(base64_decoded, private_key)
    return decrypted.decode("utf-8")


def main() -> None:
    private_key: RSAPrivateKey = load_private_key("private.pem")
    public_key: RSAPublicKey = private_key.public_key()

    # Example usage
    message: str = "This is a secret message."
    encrypted: bytes = encrypt(message, public_key)
    decrypted: str = decrypt(encrypted, private_key)

    print(f"Message:\n{message}\n")
    print(f"Encrypted text (base64 encoded):\n{encrypted!r}\n")
    print(f"Decrypted (UTF-8):\n{decrypted}\n")


if __name__ == "__main__":
    main()
