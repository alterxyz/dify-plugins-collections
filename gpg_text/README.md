# GPG Text Tools Plugin for Dify

This plugin provides a suite of tools for performing common GPG (GNU Privacy Guard) operations on text directly within Dify, utilizing the `pgpy` Python library. It allows users and AI agents to encrypt, decrypt, sign, and verify messages, as well as generate new GPG key pairs.

## Features

The plugin includes the following tools:

1.  **GPG Encrypt Message (`encrypt_message`)**: Encrypts a plaintext message using a recipient's GPG public key.
2.  **GPG Decrypt Message (`decrypt_message`)**: Decrypts a GPG-encrypted message using the recipient's private key and optional passphrase.
3.  **GPG Sign Message (`sign_message`)**: Creates a detached GPG signature for a plaintext message using the signer's private key and optional passphrase.
4.  **GPG Verify Signature (`verify_message`)**: Verifies a detached GPG signature against the original message using the signer's public key.
5.  **GPG Generate Key Pair (`generate_key_pair`)**: Generates a new GPG key pair (public and private keys) with specified user details and optional parameters.

## Setup

No specific setup is required beyond adding the plugin to Dify. The necessary `pgpy` library is included in the plugin's requirements.

## Usage

Each tool requires specific inputs, typically provided as parameters within Dify.

### 1. Encrypt Message

*   **Parameters**:
    *   `plaintext`: The text message you want to encrypt.
    *   `recipient_pubkey_str`: The recipient's full ASCII-armored GPG public key block.
*   **Output**: The encrypted message in ASCII-armored PGP format.

### 2. Decrypt Message

*   **Parameters**:
    *   `encrypted_message_str`: The full ASCII-armored PGP encrypted message block.
    *   `private_key_str`: Your full ASCII-armored GPG private key block. **Handle with extreme care.**
    *   `passphrase` (Optional): The passphrase protecting your private key, if applicable.
*   **Output**: The decrypted plaintext message.

### 3. Sign Message

*   **Parameters**:
    *   `message_to_sign`: The text message you want to sign.
    *   `signer_private_key_str`: Your full ASCII-armored GPG private key block used for signing. **Handle with extreme care.**
    *   `passphrase` (Optional): The passphrase protecting your private key, if applicable.
*   **Output**: The detached ASCII-armored GPG signature.

### 4. Verify Signature

*   **Parameters**:
    *   `original_message`: The original plaintext message that was signed.
    *   `signature_blob`: The detached ASCII-armored GPG signature block.
    *   `signer_pubkey_str`: The signer's full ASCII-armored GPG public key block.
*   **Output**: A boolean value (`true` or `false`) indicating if the signature is valid, along with a descriptive text message.

### 5. Generate Key Pair

*   **Parameters**:
    *   `real_name`: The name to associate with the key (e.g., "Alice Wonderland").
    *   `email`: The email address to associate with the key (e.g., "alice@example.com").
    *   `passphrase` (Optional): A passphrase to protect the generated private key. Highly recommended.
    *   `key_type` (Optional): The primary key algorithm (e.g., `EdDSA`, `RSAEncryptOrSign`). Defaults to `EdDSA`.
    *   `key_param` (Optional): Key length (for RSA/DSA) or curve name (for ECC). Defaults depend on `key_type`.
*   **Output**: The generated public key and private key in ASCII-armored format. **Securely store the private key and passphrase immediately.**

## Security Considerations

*   **Private Key Handling**: Private keys and passphrases are highly sensitive. This plugin requires them as direct input parameters for decryption and signing. Be extremely cautious about how and where you provide this information within Dify. Avoid storing them directly in prompts or workflow configurations if possible. Consider using secure credential management features if available in your Dify setup.
*   **No Key Storage**: This plugin does not store any keys or passphrases beyond the immediate execution scope of a tool invocation. The responsibility for secure key management lies entirely with the user.
*   **Generated Keys**: When generating keys, immediately copy and securely store the private key and its passphrase outside of Dify. The plugin will output them, but does not retain them.

## Underlying Library

This plugin uses the [pgpy](https://pgpy.readthedocs.io/en/latest/) library for all cryptographic operations.



