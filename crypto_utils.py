import os
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature, InvalidTag

def generate_symmetric_key():
    """Generates a 256-bit key for AES-GCM."""
    return AESGCM.generate_key(bit_length = 256)

def symmetric_encrypt_gcm(key, plaintext_bytes, associated_data = None) -> bytes:
    """
    Encrypts plaintext using AES-GCM. Returns nonce + ciphertext. Nonce is 12 bytes, prepended.
    """
    if not isinstance(plaintext_bytes, bytes):
        raise TypeError("plaintext_bytes must be bytes")
    if associated_data is not None and not isinstance(associated_data, bytes):
        raise TypeError("associated_data must be bytes or None")

    nonce = os.urandom(12) # AES-GCM standard nonce size
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext_bytes, associated_data)
    return nonce + ciphertext

def symmetric_decrypt_gcm(key, nonce_ciphertext_bytes, associated_data = None) -> bytes | None:
    """
    Decrypts AES-GCM encrypted data (nonce + ciphertext).
    Extracts 12-byte nonce from the beginning.
    Returns plaintext_bytes or None if decryption fails.
    """
    if not isinstance(nonce_ciphertext_bytes, bytes):
        raise TypeError("nonce_ciphertext_bytes must be bytes")
    if associated_data is not None and not isinstance(associated_data, bytes):
        raise TypeError("associated_data must be bytes or None")
    
    nonce = nonce_ciphertext_bytes[:12]
    ciphertext = nonce_ciphertext_bytes[12:]
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
        return plaintext
    except InvalidTag:
        print("Decryption failed: Invalid authentication tag (data integrity compromised).")
        return None
    
def load_private_key(key_file_path, password = None) -> PrivateKeyTypes:
    """Loads a PEM-encoded private key."""
    with open(key_file_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password = password.encode() if password else None,
        )
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise TypeError("Loaded key is not an RSA private key.")
    return private_key

def load_public_key_and_id_from_certificate_file(cert_path: str) -> tuple[rsa.RSAPublicKey, str | bytes]:
    """Loads a PEM-encoded X.509 certificate and returns its public key and user id."""
    # TODO: find actual return type and fix the user_id list return
    with open(cert_path, "rb") as cert_file:
        cert = x509.load_pem_x509_certificate(cert_file.read())
    public_key = cert.public_key()
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TypeError("Extracted public key is not an RSA public public key.")
    user_id = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
    print(f"DEBUG-HERE: user_id raw: {user_id}")
    if not user_id:
        raise ValueError("No Common Name (CN) found in the certificate's subject.")
    return (public_key, user_id[0].value)

def asymmetric_encrypt_oaep(public_key: rsa.RSAPublicKey, data: bytes) -> bytes:
    """Encrypts data_bytes using RSA-OAEP with the given public_key."""
    # FIX: not needed check if you type hint it in the definition
    # if not isinstance(data, bytes):
    #     raise TypeError("data_bytes for asymmetric encryption must be bytes.")
    ciphertext = public_key.encrypt(
        data,
        asym_padding.OAEP(
            mgf = asym_padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )
    return ciphertext

def asymmetric_decrypt_oaep(private_key, ciphertext_bytes):
    """Decrypts ciphertext_bytes using RSA-OAEP with the given private_key."""
    if not isinstance(ciphertext_bytes, bytes):
        raise TypeError("ciphertext_bytes for asymmetric decryption must be bytes.")
    try:
        plaintext = private_key.decrypt(
            ciphertext_bytes,
            asym_padding.OAEP(
                mgf = asym_padding.MGF1(algorithm = hashes.SHA256()),
                algorithm = hashes.SHA256(),
                label = None
            )
        )
        return plaintext
    except ValueError:
        print("Asymmetric decryption failed (ValueError, possibly incorrect key or malformed data).")
        return None

def sign_data_pss(private_key, data_to_sign_bytes):
    """Signs data_to_sign_bytes using RSA-PSS with the given private_key."""
    if not isinstance(data_to_sign_bytes, bytes):
        raise TypeError("data_to_sign_bytes must be bytes.")
    signature = private_key.sign(
        data_to_sign_bytes,
        asym_padding.PSS(
            mgf = asym_padding.MGF1(hashes.SHA256()),
            salt_length = asym_padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature_pss(public_key, signature_bytes, data_that_was_signed_bytes):
    """Verifies a signature using RSA-PSS."""
    if not isinstance(signature_bytes, bytes) or not isinstance(data_that_was_signed_bytes, bytes):
        raise TypeError("Signature and data for verification must be bytes.")
    try:
        public_key.verify(
            signature_bytes,
            data_that_was_signed_bytes,
            asym_padding.PSS(
                mgf = asym_padding.MGF1(hashes.SHA256()),
                salt_length = asym_padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        print("Signature verification failed: Signature is invalid.")
        return False
    except Exception as e:
        print(f"An unexpected error occured during signature verification: {e}")
        return False
