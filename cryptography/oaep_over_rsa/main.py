from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def oaep_encrypt(message, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    ciphertext = cipher.encrypt(message)
    return ciphertext


def oaep_decrypt(ciphertext, private_key):
    cipher = PKCS1_OAEP.new(private_key)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext


def main():
    # Generate RSA key pair
    key = RSA.generate(2048)
    public_key = key.publickey()
    private_key = key

    # Message to be encrypted
    message = b"Hello, World!"

    # Encrypt message
    ciphertext = oaep_encrypt(message, public_key)
    print("Ciphertext:", ciphertext.hex())

    # Decrypt message
    decrypted_message = oaep_decrypt(ciphertext, private_key)
    print("Decrypted message:", decrypted_message.decode())


if __name__ == "__main__":
    main()
