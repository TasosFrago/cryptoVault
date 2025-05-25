import os
import shutil
import app_utils
import crypto_utils

BASE_STORAGE_PATH = app_utils.resource_path("vault_data")
VAULT_PRIVATE_KEY_PATH = app_utils.resource_path("crypto_materials/vault_private_key.key")
VAULT_CERT_PATH = app_utils.resource_path("crypto_materials/vault_certificate.crt")
VAULT_KEY_PASSWORD = None

class Vault:
    def __init__(self):
        os.makedirs(BASE_STORAGE_PATH, exist_ok = True)
        try:
            self.private_key = crypto_utils.load_private_key(VAULT_PRIVATE_KEY_PATH, VAULT_KEY_PASSWORD)
            [self.public_key, _] = crypto_utils.load_public_key_and_id_from_certificate_file(VAULT_CERT_PATH)
        except Exception as e:
            raise Exception(f"Failed to initialize Vault keys: {e}")
        print("Vault initialized with its cryptographic keys.")

    def register_user(self, username: str, cert_path: str) -> None:
        [_, user_id] = crypto_utils.load_public_key_and_id_from_certificate_file(cert_path)
        folder_name = f"{user_id}-{username}"
        user_folder = os.path.join(BASE_STORAGE_PATH, folder_name)
        print(user_folder)
        os.makedirs(user_folder, exist_ok = True)
        print(f"User '{username}' registered. Storage folder created at {user_folder}")

    def store_file(
        self,
        folder_name: str,
        user_uploaded_enc_path: str,
        user_uploaded_enc_sym_key_path: str,
        original_filename_tag: str
    ) -> bool:
        username = folder_name.split("-", 1)[1]
        user_folder = os.path.join(BASE_STORAGE_PATH, folder_name)
        if not os.path.exists(user_folder):
            print(f"Error: User '{username}' not registered.")
            return False

        base_stored_filename = os.path.join(user_folder, original_filename_tag)
        stored_encrypted_data_path = f"{base_stored_filename}.data.enc"
        stored_encrypted_sym_key_path = f"{base_stored_filename}.symkey.enc"
        vault_signature_path = f"{base_stored_filename}.sig"

        try:
            shutil.copy(user_uploaded_enc_path, stored_encrypted_data_path)
            shutil.copy(user_uploaded_enc_sym_key_path, stored_encrypted_sym_key_path)

            # concatenate the two stored encrypted files (as bytes) for signing
            data_to_sign_bytes = b""
            with open(stored_encrypted_data_path, "rb") as f_data:
                data_to_sign_bytes += f_data.read()
            with open(stored_encrypted_sym_key_path, "rb") as f_key:
                data_to_sign_bytes += f_key.read()

            # sign using Vault's private key
            signature_bytes = crypto_utils.sign_data_pss(self.private_key, data_to_sign_bytes)
            with open(vault_signature_path, 'wb') as f_sig:
                f_sig.write(signature_bytes)

            print(f"Stored for '{username}': {original_filename_tag} (data, key, signature)")
            return True

        except Exception as e:
            print(f"Error storing file for '{username}': {e}")
            # clean partial files if error occurred
            if os.path.exists(stored_encrypted_data_path): os.remove(stored_encrypted_data_path)
            if os.path.exists(stored_encrypted_sym_key_path): os.remove(stored_encrypted_sym_key_path)
            if os.path.exists(vault_signature_path): os.remove(vault_signature_path)
            return False
    
    def retrieve_file(self, folder_name: str, original_filename_tag: str) -> tuple[str|None, str|None, str|None, str]:
        username = folder_name.split("-", 1)[1]
        user_folder = os.path.join(BASE_STORAGE_PATH, folder_name)
        if not os.path.exists(user_folder):
            print(f"Error: User '{username}' not registered.")
            return None, None, None, "User not registered."

        base_stored_filename = os.path.join(user_folder, original_filename_tag)
        stored_encrypted_data_path = f"{base_stored_filename}.data.enc"
        stored_encrypted_sym_key_path = f"{base_stored_filename}.symkey.enc"
        vault_signature_path = f"{base_stored_filename}.sig"

        if not all(os.path.exists(p) for p in [stored_encrypted_data_path, stored_encrypted_sym_key_path, vault_signature_path]):
            return None, None, None, "Error: Requested file components not found."

        try:
            # concatenate stored files for verification
            data_that_was_signed_bytes = b""
            with open(stored_encrypted_data_path, "rb") as f_data:
                data_that_was_signed_bytes += f_data.read()
            with open(stored_encrypted_sym_key_path, "rb") as f_key:
                data_that_was_signed_bytes += f_key.read()
            with open(vault_signature_path, "rb") as f_sig:
                signature_bytes = f_sig.read()

            # verify integrity using Vault's public key
            is_valid = crypto_utils.verify_signature_pss(self.public_key, signature_bytes, data_that_was_signed_bytes)

            if not is_valid:
                print(f"Integrity Check FAILED by Vault for {original_filename_tag} of user {username}.")
                return stored_encrypted_data_path, stored_encrypted_sym_key_path, vault_signature_path, "Integrity check failed by Vault. Files may have been tampered."

            print(f"Integrity Check PASSED by Vault for {original_filename_tag} of user {username}.")
            return stored_encrypted_data_path, stored_encrypted_sym_key_path, None, "Files retrieved successfully."

        except Exception as e:
            print(f"Error during Vault's file retrieval or verification: {e}")
            return None, None, None, f"Vault-side error during retrieval: {e}"

    def list_user_files(self, user_vault_folder_name: str) -> list[str]:
        user_specific_vault_path = os.path.join(BASE_STORAGE_PATH, user_vault_folder_name)
        if not os.path.exists(user_specific_vault_path):
            return []

        files = []
        for f_name in os.listdir(user_specific_vault_path):
            if f_name.endswith(".data.enc"):
                original_tag = f_name[:-len(".data.enc")]
                if os.path.exists(os.path.join(user_specific_vault_path, f"{original_tag}.symkey.enc")) and \
                    os.path.exists(os.path.join(user_specific_vault_path, f"{original_tag}.sig")):
                    if original_tag not in files:
                        files.append(original_tag)
        print(f"[Vault] Listing files for '{user_vault_folder_name}': {files}")
        return files
