# Privacy Policy for GPG Text Tools Plugin

This document outlines how the GPG Text Tools plugin for Dify handles data.

## Data Processed

The plugin processes the following types of data based on the tool being used:

*   **Plaintext Messages**: Text provided by the user for encryption or signing.
*   **Encrypted Messages**: PGP-formatted encrypted data provided for decryption.
*   **Signatures**: PGP-formatted detached signatures provided for verification.
*   **GPG Keys (Public and Private)**: ASCII-armored public and private keys provided by the user for encryption, decryption, signing, or verification.
*   **Key Passphrases**: Passphrases provided by the user to unlock protected private keys.
*   **User Information for Key Generation**: Real name and email address provided by the user when generating a new key pair.

## Data Processing Location

All data processing, including cryptographic operations (encryption, decryption, signing, verification, key generation), occurs entirely within the Dify plugin execution environment. No data is sent to external third-party services for processing by this plugin itself.

## Data Storage and Persistence

*   **No Long-Term Storage**: The plugin does **not** store any user-provided data (messages, keys, passphrases) beyond the scope of a single tool execution. Once the tool finishes its operation, the data used during that execution is discarded from the plugin's memory.
*   **User Responsibility**: The secure storage and management of GPG keys and passphrases are the sole responsibility of the user. This plugin acts as a transient processor and does not provide key management or storage capabilities.

## Third-Party Libraries

The plugin utilizes the `pgpy` Python library to perform GPG operations locally within the execution environment. It does not interact with external network services.

## Security

While the plugin uses established cryptographic libraries, the security of your data heavily relies on how you manage your GPG keys and passphrases. Avoid exposing sensitive private keys or passphrases in insecure ways when interacting with the plugin.