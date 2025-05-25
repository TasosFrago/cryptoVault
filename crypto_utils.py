import os
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidSignature, InvalidTag

def generate_symmetric_key() -> bytes:
    """Generates a 256-bit key for AES-GCM."""
    return AESGCM.generate_key(bit_length=256)

def symmetric_encrypt_gcm(key: bytes, plaintext: bytes, associated_data: bytes | None = None) -> bytes:
    """
    Encrypts plaintext using AES-GCM.
    Returns nonce + ciphertext. 
    Nonce is 12 bytes, prepended.
    """
    nonce = os.urandom(12) # AES-GCM standard nonce size
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data)
    return nonce + ciphertext

def symmetric_decrypt_gcm(key, nonce_ciphertext: bytes, associated_data: bytes|None = None) -> bytes | None:
    """
    Decrypts AES-GCM encrypted data (nonce + ciphertext).
    Extracts 12-byte nonce from the beginning.
    Returns plaintext_bytes or None if decryption fails.
    """
    nonce = nonce_ciphertext[:12]
    ciphertext = nonce_ciphertext[12:]
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data)
        return plaintext
    except InvalidTag:
        print("Decryption failed: Invalid authentication tag (data integrity compromised).")
        return None
    
def load_private_key(key_path: str, password: str|None = None) -> rsa.RSAPrivateKey:
    """Loads a PEM-encoded private key."""
    with open(key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password = password.encode() if password else None,
        )
    if not isinstance(private_key, rsa.RSAPrivateKey):
        raise TypeError("Loaded key is not an RSA private key.")
    return private_key

def load_public_key_and_id_from_certificate_file(cert_path: str) -> tuple[rsa.RSAPublicKey, str | bytes]:
    """Loads a PEM-encoded X.509 certificate and returns its public key and user id."""
    with open(cert_path, "rb") as cert_file:
        cert = x509.load_pem_x509_certificate(cert_file.read())

    public_key = cert.public_key()
    if not isinstance(public_key, rsa.RSAPublicKey):
        raise TypeError("Extracted public key is not an RSA public public key.")

    [user_id] = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
    if not user_id:
        raise ValueError("No Common Name (CN) found in the certificate's subject.")
    return (public_key, user_id.value)

def asymmetric_encrypt_oaep(public_key: rsa.RSAPublicKey, data: bytes) -> bytes:
    """Encrypts data_bytes using RSA-OAEP with the given public_key."""
    ciphertext = public_key.encrypt(
        data,
        asym_padding.OAEP(
            mgf = asym_padding.MGF1(algorithm = hashes.SHA256()),
            algorithm = hashes.SHA256(),
            label = None
        )
    )
    return ciphertext

def asymmetric_decrypt_oaep(private_key: rsa.RSAPrivateKey, ciphertext: bytes) -> bytes | None:
    """Decrypts ciphertext_bytes using RSA-OAEP with the given private_key."""
    try:
        plaintext = private_key.decrypt(
            ciphertext,
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

def sign_data_pss(private_key: rsa.RSAPrivateKey, data_to_sign: bytes) -> bytes:
    """Signs data_to_sign_bytes using RSA-PSS with the given private_key."""
    signature = private_key.sign(
        data_to_sign,
        asym_padding.PSS(
            mgf = asym_padding.MGF1(hashes.SHA256()),
            salt_length = asym_padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature_pss(public_key: rsa.RSAPublicKey, signature: bytes, data_that_was_signed: bytes) -> bool:
    """Verifies a signature using RSA-PSS."""
    try:
        public_key.verify(
            signature,
            data_that_was_signed,
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
