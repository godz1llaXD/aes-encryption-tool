# AES-256 Text Encryption Tool

##  Overview
This project is a **secure text encryption and decryption application** built using **AES-256 (Advanced Encryption Standard)**. It provides a simple graphical interface for encrypting sensitive data using a password-derived key.

The tool is designed to be:
- **Secure** – Uses industry-standard AES-256 encryption
- **Offline** – No internet dependency
- **User-Friendly** – Clean GUI built with Kivy/KivyMD
- **Lightweight** – Fast and minimal resource usage

---

## Features
-  AES-256 Encryption & Decryption
-  Password-based key derivation (PBKDF2)
-  Clipboard support (copy/paste encrypted or decrypted text)
-  Interactive GUI interface
-  Fast and responsive performance
-  Basic validation and error handling

---

## How It Works
1. User enters plaintext and a password
2. Password is converted into a secure key using **PBKDF2**
3. AES-256 algorithm encrypts the text using:
   - Derived key
   - Initialization Vector (IV)
4. Encrypted output is generated
5. Decryption reverses the process using the same password

---

## Tech Stack

| Component        | Technology Used        |
|----------------|----------------------|
| Language        | Python               |
| GUI Framework   | Kivy, KivyMD         |
| Cryptography    | PyCryptodome         |
| Key Derivation  | PBKDF2               |

---

## Project Structure

AES-256-Encryption-Tool/

│

├── main.py # Main application logic

├── ui.kv # Kivy UI layout

├── encryption.py # Encryption/Decryption logic

├── requirements.txt # Dependencies

└── README.md # Project documentation


---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/aes256-encryption-tool.git
cd aes256-encryption-tool
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python main.py
```

---

### Future Enhancements
- File encryption & decryption support
- Convert to executable (.exe)
- Mobile app (APK using Kivy)
- Web-based interface (Flask/React)
- Enhanced security features (HMAC, integrity checks)

---

### Security Notes
- This tool uses strong encryption, but:
  - Weak passwords reduce security
  - Do not reuse passwords across sensitive platforms
- Currently intended for educational and demonstration purposes

---

### Use Cases
- Secure storage of sensitive notes
- Learning cryptographic implementations
- Demonstrating encryption concepts in interviews/projects

---

### Example

## Input:
```bash
Text: HelloWorld
Password: mysecurepassword
```
## Output:
```bash
Encrypted: U2FsdGVkX1+...
```

---

### Screenshots

---

### License

This project is licensed under the MIT License.

---

### Author

Godz1lla
- GitHub: https://github.com/godz1llaXD

---

### Acknowledgements

- PyCryptodome for cryptographic functions
- Kivy & KivyMD for GUI framework

---

### Feedback

If you have suggestions or improvements, feel free to open an issue or contribute.

---
