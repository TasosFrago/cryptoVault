import os

import crypto.app_utils
from crypto import crypto_utils
from crypto.vault_logic import Vault

TEMP_DIR = crypto.app_utils.resource_path("../temp_user_files")
VAULT_CERT_PATH = crypto.app_utils.resource_path("../crypto_materials/vault_certificate.crt")

class User:
    def __init__(
        self,
        username_alias: str, # Username given by then user
        cert_path: str
    ) -> None:
        self.username_alias: str = username_alias
        self.cert_file_path: str = cert_path
        os.makedirs(TEMP_DIR, exist_ok=True)

        try:
            [public_key, user_id] = crypto_utils.load_public_key_and_id_from_certificate_file(cert_path)
            self.public_key = public_key
            self.user_id = user_id
            self.vault_folder = f"{self.user_id}-{self.username_alias}"
            print(f"User '{self.username_alias}' (ID from Certificate CN: '{self.user_id}', Vault Folder: {self.vault_folder}) initialized.")
        except Exception as e:
            uid_for_error = self.user_id if hasattr(self, 'user_id') else 'N/A'
            raise Exception(f"Failed to initialize User '{username_alias}' (ID from Certificate CN: {uid_for_error}): {e}")

    def store_file(self, vault_instance: Vault, input_plaintext_path: str) -> bool:
        """
        User encrypts a file, encrypts the symmetric key with their own public key, 
        and asks the vault to store them in their designated folder.
        """
        original_filename_tag = os.path.basename(input_plaintext_path)
        tmp_encrypted_data_file = os.path.join(TEMP_DIR, f"{self.username_alias}_{original_filename_tag}.data.enc")
        tmp_encSymKey_path = os.path.join( TEMP_DIR, f"{self.username_alias}_{original_filename_tag}.symkey.enc")

        try:
            # read plaintext file
            with open(input_plaintext_path, "rb") as f_plain:
                plaintext = f_plain.read()

            # generate a new symmetric key
            symmetric_key = crypto_utils.generate_symmetric_key()

            # symmetrically encrypt the plaintext
            nonce_plus_encrypted_data = crypto_utils.symmetric_encrypt_gcm(symmetric_key, plaintext)

            with open(tmp_encrypted_data_file, "wb") as f_enc_data:
                f_enc_data.write(nonce_plus_encrypted_data)

            # asymmetrically encrypt the symmetric key with the user's own public key
            encrypted_symmetric_key = crypto_utils.asymmetric_encrypt_oaep(self.public_key, symmetric_key)

            with open(tmp_encSymKey_path, 'wb') as f_enc_sym_key:
                f_enc_sym_key.write(encrypted_symmetric_key)

            print(f"User '{self.username_alias}' prepared file '{original_filename_tag}' for vault storage.")

            # deliver to vault for storage
            success = vault_instance.store_file(
                self.vault_folder,
                tmp_encrypted_data_file,
                tmp_encSymKey_path,
                original_filename_tag
            )
 
            # clean up temporary files
            if os.path.exists(tmp_encrypted_data_file): os.remove(tmp_encrypted_data_file)
            if os.path.exists(tmp_encSymKey_path): os.remove(tmp_encSymKey_path)

            if success:
                print(f"File '{original_filename_tag}' successfully sent to vault by user '{self.username_alias}'.")
            else:
                print(f"Vault failed to store file '{original_filename_tag}' for user '{self.username_alias}'.")

            return success

        except Exception as e:
            print(f"Error during User '{self.username_alias}' prepare_and_store_file for '{original_filename_tag}': {e}")

            if os.path.exists(tmp_encrypted_data_file):
                os.remove(tmp_encrypted_data_file)

            if os.path.exists(tmp_encSymKey_path):
                os.remove(tmp_encSymKey_path)

            return False

    def retrieve_decrypt_file(
        self,
        vault_instance: Vault,
        original_filename_tag: str,
        private_key_path: str,
        private_key_password: str|None = None
    ) -> str | None:
        """
        User requests a file from the vault using their vault_folder, 
        receives encrypted data and key, decrypts them using private key.
        """
        # request file from the vault
        [ret_enc_data_path, ret_enc_sym_key_path, vault_sig_path, message] = vault_instance.retrieve_file(self.vault_folder, original_filename_tag)
        print(f"\nUser '{self.username_alias}' received response from Vault for '{original_filename_tag}': {message}")

        if not ret_enc_data_path or not ret_enc_sym_key_path:
            print(f"User '{self.username_alias}' could not retrieve necessary file components for '{original_filename_tag}'.")
            return None

        if vault_sig_path: # there is an integrity violation for Vault to respond with the signature
            print(f"Vault reported an integrity issue. User '{self.username_alias}' is now verifying with Vault's public key...")
            try:
                # load Vault's public key
                [vault_public_key, _] = crypto_utils.load_public_key_and_id_from_certificate_file(VAULT_CERT_PATH)

                data_that_was_signed = b""
                with open(ret_enc_data_path, "rb") as f_data:
                    data_that_was_signed += f_data.read()

                with open(ret_enc_sym_key_path, "rb") as f_key:
                    data_that_was_signed += f_key.read()

                with open(vault_sig_path, "rb") as f_sig:
                    signature = f_sig.read()

                # check for tampering
                is_tampered_user_side = not crypto_utils.verify_signature_pss(vault_public_key, signature, data_that_was_signed)
                if is_tampered_user_side:
                    print(f"User '{self.username_alias}' confirms: Tampering detected based on Vault's signature and provided files.")
                else:
                    print(f"User '{self.username_alias}' verification: Signature seems valid. This is unexpected if Vault reported an integrity failure on these exact files and signature.")

            except Exception as e:
                print(f"Error during user-side verification of Vault's integrity report for '{self.username_alias}': {e}")
            return None # no decryption if integrity is violated

        try:
            # read and decrypt the symmetric key using the user's own private key
            private_key = crypto_utils.load_private_key(private_key_path, private_key_password)
            with open(ret_enc_sym_key_path, "rb") as f_enc_sym_key:
                encrypted_symmetric_key = f_enc_sym_key.read()

            decrypted_symmetric_key = crypto_utils.asymmetric_decrypt_oaep(private_key, encrypted_symmetric_key)
            if not decrypted_symmetric_key:
                print(f"User '{self.username_alias}' failed to decrypt symmetric key for '{original_filename_tag}'.")
                return None

            # read and decrypt the data file using the symmetric key
            with open(ret_enc_data_path, "rb") as f_enc_data:
                nonce_plus_encrypted_data = f_enc_data.read()

            original_data = crypto_utils.symmetric_decrypt_gcm(decrypted_symmetric_key, nonce_plus_encrypted_data)
            if not original_data:
                print(f"User '{self.username_alias}' failed to decrypt data file for '{original_filename_tag}' (integrity tag mismatch or other AES-GCM decryption error).")
                return None
            print(f"File '{original_filename_tag}' successfully decrypted by user '{self.username_alias}'.")

            # read the file
            output_plaintext_path = os.path.join(TEMP_DIR, f"{self.username_alias}_{original_filename_tag}")
            with open(output_plaintext_path, "wb") as f_out:
                f_out.write(original_data)

            print(f"Decrypted content for '{original_filename_tag}' saved to: {output_plaintext_path}")
            print("\n--- Decrypted File Content (first 200 chars) ---")

            try:
                print(original_data[:200].decode("utf-8", errors="replace"))
            except Exception: # print raw data if decode fails
                print(original_data[:200])
            print("--- End of Preview ---\n")

            return output_plaintext_path

        except FileNotFoundError as fnf_error:
            print(f"Error during User '{self.username_alias}' retrieve_and_decrypt_file for '{original_filename_tag}': Missing file {fnf_error.filename}")
            return None
        except Exception as e:
            print(f"Error during User '{self.username_alias}' retrieve_and_decrypt_file for '{original_filename_tag}': {e}")
            return None
