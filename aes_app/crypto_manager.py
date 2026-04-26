# crypto_manager.py
import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

def encrypt(text: str, password: str) -> str:
    """
    Encrypts a string using AES-256-GCM.
    
    Args:
        text (str): The plaintext string to encrypt.
        password (str): The password used to derive the encryption key.
        
    Returns:
        str: Base64 encoded string containing Salt + Nonce + Ciphertext + Tag.
    """
    salt = get_random_bytes(16)
    nonce = get_random_bytes(16)
    
    # Derive 32-byte key (AES-256)
    key = PBKDF2(password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    
    # Encode string to bytes before encrypting
    ciphertext, tag = cipher.encrypt_and_digest(text.encode('utf-8'))
    
    # Concatenate all components and encode to base64
    payload = salt + nonce + ciphertext + tag
    return base64.b64encode(payload).decode('utf-8')

def decrypt(encrypted_text: str, password: str) -> str:
    """
    Decrypts an AES-256-GCM encrypted string.
    
    Args:
        encrypted_text (str): Base64 encoded payload.
        password (str): The password used for decryption.
        
    Returns:
        str: The decrypted plaintext string.
        
    Raises:
        ValueError: If MAC verification fails (wrong password or data tampering) or payload is invalid.
    """
    try:
        raw = base64.b64decode(encrypted_text)
        
        # Minimum payload length: Salt(16) + Nonce(16) + Tag(16) = 48 bytes
        if len(raw) < 48:
            raise ValueError("Invalid payload: too short.")
            
        salt = raw[:16]
        nonce = raw[16:32]
        
        # Tag is the last 16 bytes
        tag = raw[-16:]
        
        # Ciphertext is everything in between
        ciphertext = raw[32:-16]
        
        # Derive key
        key = PBKDF2(password, salt, dkLen=32, count=1000000, hmac_hash_module=SHA256)
        
        cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
        
        # Decrypt and verify. This raises ValueError if tag verification fails.
        decrypted_bytes = cipher.decrypt_and_verify(ciphertext, tag)
        
        return decrypted_bytes.decode('utf-8')
    except (ValueError, KeyError) as e:
        raise ValueError(f"Decryption failed: {str(e)}")
    except Exception as e:
        raise ValueError(f"Invalid format or corrupted data: {str(e)}")
