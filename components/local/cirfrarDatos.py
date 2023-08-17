import rsa
import base64
import json

class RSAEncryption:

    @staticmethod
    def decrypt_asymmetric(encoded_message, private_key_pem):
        try:
            # Convert PEM to PrivateKey
            private_key = rsa.PrivateKey.load_pkcs1(private_key_pem.encode())

            # Decode from base64 and Decrypt
            decoded_message = base64.b64decode(encoded_message)
            decrypted_message = rsa.decrypt(decoded_message, private_key)
            
            return json.loads(decrypted_message.decode())
        except Exception as e:
            raise e

    @staticmethod
    def encrypt_asymmetric(message, public_key_pem):
        try:
            # Convert message to string and encode
            msg_str = json.dumps(message).encode()

            # Convert PEM to PublicKey
            public_key = rsa.PublicKey.load_pkcs1_openssl_pem(public_key_pem.encode())

            # Encrypt and encode to base64
            encrypted_message = rsa.encrypt(msg_str, public_key)
            encoded_message = base64.b64encode(encrypted_message)
            
            return encoded_message.decode()
        except Exception as e:
            raise e

# Example usage:
private_key_pem, public_key_pem = rsa.newkeys(512)  # Generate new keys
private_key_pem = private_key_pem.save_pkcs1().decode()
public_key_pem = public_key_pem.save_pkcs1().decode()

encrypted_message = RSAEncryption.encrypt_asymmetric({"msg": "Hello"}, public_key_pem)
print("Encrypted:", encrypted_message)

# decrypted_message = RSAEncryption.decrypt_asymmetric(encrypted_message, private_key_pem)
# print("Decrypted:", decrypted_message)
